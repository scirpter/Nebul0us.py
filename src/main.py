from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocketState

from base.app import App
from game.api import CoinPurchase, DeleteAccount
from game.enums.game_mode import GAME_MODE
from game.enums.regions import REGION
from game.models.client.client import Client
from helpers.config_integrity import save_config

PRIMARY_COLOR = "#c084fc"      # soft purple
SECONDARY_COLOR = "#f5f5f6"    # soft white
TERTIARY_COLOR = "#a855f7"     # deeper purple accent
BACKGROUND_COLOR = "#0d0c11"   # charcoal base
SURFACE_COLOR = "#14131b"      # charcoal surface

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app_state = App()
app = FastAPI(title="2oh Console")
websocket_clients: set[WebSocket] = set()

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _shell_summary() -> dict[str, Any]:
    total = len(app_state.clients)
    connected = sum(1 for c in app_state.clients if getattr(c, "is_connected", False))
    notifications = list(app_state.states["cache"].get("notifications", []))
    return {
        "total_clients": total,
        "connected_clients": connected,
        "notifications": notifications[-5:],
    }


def _devlogs(limit: int = 50) -> list[dict[str, Any]]:
    entries = app_state.devlog_entries[-limit:]
    return [
        {
            "timestamp": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "message": e.message,
            "importance": e.importance,
        }
        for e in reversed(entries)
    ]


def _recent_notifications(limit: int = 20) -> list[dict[str, Any]]:
    notes = app_state.states["cache"].get("notifications", [])
    total = len(notes)
    start_index = max(0, total - limit)
    result: list[dict[str, Any]] = []
    for idx, n in enumerate(notes[-limit:], start=start_index):
        result.append(
            {
                "uid": idx,
                "title": n.get("title", ""),
                "message": n.get("message", ""),
            }
        )
    return result


def _client_status_snapshot(client: Client) -> dict[str, Any]:
    return {
        "uid": client.client_data.uid,
        "name": client.client_data.name,
        "is_connected": client.is_connected,
        "auto_respawn": client.options_data.auto_respawn,
        "chase_nearest_holes": client.options_data.chase_nearest_holes,
    }


def _client_world_snapshot(client: Client) -> dict[str, Any]:
    world = client.client_data.world
    players = []
    for pid, player in world.players.copy().items():
        average = player.get_avg_pos()
        players.append(
            {
                "id": pid,
                "name": player.name,
                "mass": player.get_mass(),
                "blobs": len(player.blobs),
                "avg_x": average.x if average else None,
                "avg_y": average.y if average else None,
            }
        )

    holes = []
    for hid, hole in world.holes.copy().items():
        holes.append(
            {
                "id": hid,
                "type": getattr(hole.type, "name", str(hole.type)),
                "mass": hole.mass,
                "x": hole.pos.x,
                "y": hole.pos.y,
                "present": hole.is_present(),
            }
        )

    return {
        "uid": client.client_data.uid,
        "name": client.client_data.name,
        "is_connected": client.is_connected,
        "players": players,
        "holes": holes,
    }


async def _live_status_loop() -> None:
    while True:
        await asyncio.sleep(1.0)
        _broadcast(
            {
                "type": "bots:status",
                "clients": [
                    _client_status_snapshot(client) for client in app_state.clients
                ],
                "summary": _shell_summary(),
            }
        )


async def _live_world_loop() -> None:
    while True:
        await asyncio.sleep(1.2)
        _broadcast(
            {
                "type": "world:state",
                "clients": [
                    _client_world_snapshot(client) for client in app_state.clients
                ],
            }
        )


@app.on_event("startup")
async def _start_live_tasks() -> None:
    loop = asyncio.get_event_loop()
    loop.create_task(_live_status_loop())
    loop.create_task(_live_world_loop())


def _get_client(uid: int) -> Client | None:
    for client in app_state.clients:
        if client.client_data.uid == uid:
            return client
    return None


def _broadcast(message: dict[str, Any]) -> None:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return
    for ws in list(websocket_clients):
        if ws.client_state != WebSocketState.CONNECTED:
            websocket_clients.discard(ws)
            continue
        loop.create_task(ws.send_json(message))


# wrap notify to also broadcast
_native_notify = app_state.notify


def _notify_with_ws(title: str, description: str) -> None:
    _native_notify(title, description)
    _broadcast({"type": "notification", "title": title, "message": description})


app_state.notify = _notify_with_ws  # type: ignore[assignment]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "theme": {
            "primary": PRIMARY_COLOR,
            "secondary": SECONDARY_COLOR,
            "tertiary": TERTIARY_COLOR,
            "background": BACKGROUND_COLOR,
            "surface": SURFACE_COLOR,
        },
        "summary": _shell_summary(),
        "devlogs": _devlogs(),
        "notifications": _recent_notifications(5),
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/notifications/feed")
async def notifications_feed() -> JSONResponse:
    return JSONResponse({"notifications": _recent_notifications(20)})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    websocket_clients.add(websocket)
    try:
        await websocket.send_json(
            {
                "type": "notifications:init",
                "notifications": _recent_notifications(10),
                "summary": _shell_summary(),
            }
        )
        while True:
            # keep alive; ignore incoming messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_clients.discard(websocket)
    except Exception:
        websocket_clients.discard(websocket)


@app.get("/bots", response_class=HTMLResponse)
async def bots_page(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "theme": {
            "primary": PRIMARY_COLOR,
            "secondary": SECONDARY_COLOR,
            "tertiary": TERTIARY_COLOR,
            "background": BACKGROUND_COLOR,
            "surface": SURFACE_COLOR,
        },
        "clients": app_state.clients,
        "regions": REGION.all(),
        "modes": GAME_MODE.all(),
        "summary": _shell_summary(),
    }
    return templates.TemplateResponse("bots.html", context)


@app.post("/bots/add")
async def add_bot(request: Request) -> RedirectResponse:
    form = await request.form()
    name = (form.get("name") or "").strip()
    ticket = (form.get("ticket") or "").strip()
    if not name or not ticket:
        app_state.notify("Add Bot", "Bot name and ticket are required")
        return RedirectResponse(url="/bots", status_code=303)
    if any(c.client_data.name == name for c in app_state.clients):
        app_state.notify("Add Bot", "Bot with this name already exists")
        return RedirectResponse(url="/bots", status_code=303)
    if any(c.client_data.login_ticket == ticket for c in app_state.clients):
        app_state.notify("Add Bot", "Bot with this ticket already exists")
        return RedirectResponse(url="/bots", status_code=303)
    if not ticket.endswith("=") or "," not in ticket:
        app_state.notify("Add Bot", "Invalid ticket format")
        return RedirectResponse(url="/bots", status_code=303)
    account_id = ticket.split(",")[0]
    if not account_id.isdigit():
        app_state.notify("Add Bot", "Invalid ticket format")
        return RedirectResponse(url="/bots", status_code=303)

    client = Client(app_state, int(account_id), name, ticket)
    app_state.clients.append(client)
    client.setup_loops()
    app_state.notify("Add Bot", f"Added {name}")
    _broadcast({"type": "summary", "summary": _shell_summary()})
    return RedirectResponse(url="/bots", status_code=303)


@app.post("/bots/connect/{uid}")
async def connect_bot(uid: int, request: Request) -> RedirectResponse:
    form = await request.form()
    region = form.get("region") or REGION.EU.name
    mode = form.get("mode") or GAME_MODE.FFA_ULTRA.name
    mayhem = form.get("mayhem") == "on"
    private_search = form.get("private") == "on"
    client = _get_client(uid)
    if not client:
        app_state.notify("Connect", "Client not found")
        return RedirectResponse(url="/bots", status_code=303)
    try:
        gm = GAME_MODE.from_string(mode)
    except Exception:
        gm = GAME_MODE.FFA_ULTRA
    client.settings["game_mode"] = gm.name
    result = client.connect(
        region=region,
        game_mode=gm,
        connect_in_private_search=private_search,
        mayhem=mayhem,
    )
    if isinstance(result, Exception):
        app_state.notify("Connect", f"Error: {result}")
    else:
        app_state.notify("Connect", f"Connecting {client.client_data.name}...")
    _broadcast({"type": "summary", "summary": _shell_summary()})
    return RedirectResponse(url="/bots", status_code=303)


@app.post("/bots/disconnect/{uid}")
async def disconnect_bot(uid: int) -> RedirectResponse:
    client = _get_client(uid)
    if not client:
        app_state.notify("Disconnect", "Client not found")
    elif not client.is_connected:
        app_state.notify("Disconnect", "Bot is not connected")
    else:
        client.disconnect()
        app_state.notify("Disconnect", f"{client.client_data.name} disconnected")
    _broadcast({"type": "summary", "summary": _shell_summary()})
    return RedirectResponse(url="/bots", status_code=303)


@app.post("/bots/start/{uid}")
async def start_bot(uid: int) -> RedirectResponse:
    client = _get_client(uid)
    if not client:
        app_state.notify("Start", "Client not found")
    elif not client.is_connected:
        app_state.notify("Start", "Bot is not connected")
    else:
        client.start_playing()
        app_state.notify("Player", f"{client.client_data.name} sent play request")
    return RedirectResponse(url="/bots", status_code=303)


@app.post("/bots/delete/{uid}")
async def delete_bot(uid: int) -> RedirectResponse:
    client = _get_client(uid)
    if not client:
        app_state.notify("Delete", "Client not found")
        return RedirectResponse(url="/bots", status_code=303)
    try:
        app_state.clients.remove(client)
    except ValueError:
        pass
    for setting in list(app_state.states["client_settings"]):
        if setting["client_uid"] == client.client_data.uid:
            app_state.states["client_settings"].remove(setting)
            break
    app_state.notify("Delete", f"Removed {client.client_data.name}")
    _broadcast({"type": "summary", "summary": _shell_summary()})
    return RedirectResponse(url="/bots", status_code=303)


@app.post("/bots/rename/{uid}")
async def rename_bot(uid: int, request: Request) -> RedirectResponse:
    form = await request.form()
    new_name = (form.get("name") or "").strip()
    client = _get_client(uid)
    if not client:
        app_state.notify("Rename", "Client not found")
        return RedirectResponse(url="/bots", status_code=303)
    if not new_name:
        app_state.notify("Rename", "Name cannot be empty")
        return RedirectResponse(url="/bots", status_code=303)
    if len(new_name) > 12:
        app_state.notify("Rename", "Name must be 12 characters or less")
        return RedirectResponse(url="/bots", status_code=303)
    if any(other.client_data.name == new_name and other is not client for other in app_state.clients):
        app_state.notify("Rename", "Bot with this name already exists")
        return RedirectResponse(url="/bots", status_code=303)

    client.client_data.name = new_name
    client.settings["player_name"] = new_name
    app_state.notify("Rename", f"Renamed bot to {new_name}")
    save_config(app_state.states)
    _broadcast({"type": "summary", "summary": _shell_summary()})
    return RedirectResponse(url="/bots", status_code=303)


@app.post("/bots/update-ticket/{uid}")
async def update_ticket(uid: int, request: Request) -> RedirectResponse:
    form = await request.form()
    new_ticket = (form.get("ticket") or "").strip()
    client = _get_client(uid)
    if not client:
        app_state.notify("Ticket", "Client not found")
        return RedirectResponse(url="/bots", status_code=303)
    if not new_ticket:
        app_state.notify("Ticket", "Ticket cannot be empty")
        return RedirectResponse(url="/bots", status_code=303)
    if any(
        other.client_data.login_ticket == new_ticket and other is not client
        for other in app_state.clients
    ):
        app_state.notify("Ticket", "Bot with this ticket already exists")
        return RedirectResponse(url="/bots", status_code=303)
    client.client_data.login_ticket = new_ticket
    for setting in app_state.states["client_settings"]:
        if setting["client_uid"] == client.client_data.uid:
            setting["login_ticket"] = new_ticket
            break
    save_config(app_state.states)
    app_state.notify("Ticket", f"Updated ticket for {client.client_data.name}")
    return RedirectResponse(url="/bots", status_code=303)


@app.post("/bots/options/{uid}")
async def update_bot_options(uid: int, request: Request) -> JSONResponse:
    client = _get_client(uid)
    if not client:
        return JSONResponse({"error": "Client not found"}, status_code=404)

    try:
        payload = await request.json()
    except Exception:
        payload = {}

    updated = False
    if "auto_respawn" in payload:
        client.options_data.auto_respawn = bool(payload.get("auto_respawn"))
        client.settings["auto_respawn"] = client.options_data.auto_respawn
        updated = True
    if "chase_nearest_holes" in payload:
        client.options_data.chase_nearest_holes = bool(
            payload.get("chase_nearest_holes")
        )
        client.settings["chase_nearest_holes"] = (
            client.options_data.chase_nearest_holes
        )
        updated = True

    for setting in app_state.states["client_settings"]:
        if setting["client_uid"] == client.client_data.uid:
            setting["auto_respawn"] = client.options_data.auto_respawn
            setting["chase_nearest_holes"] = client.options_data.chase_nearest_holes
            break

    if updated and app_state.states["general_settings"].get("auto_save_config"):
        save_config(app_state.states)

    return JSONResponse(
        {
            "status": "ok" if updated else "no_change",
            "client": _client_status_snapshot(client),
        }
    )


@app.get("/api/bots/status")
async def bots_status() -> JSONResponse:
    return JSONResponse(
        {
            "clients": [
                _client_status_snapshot(client) for client in app_state.clients
            ],
            "summary": _shell_summary(),
        }
    )

def _selected_clients(value: str | None) -> list[Client]:
    if not app_state.clients:
        return []
    if not value or value == "ALL":
        return list(app_state.clients)
    try:
        uid = int(value)
    except (TypeError, ValueError):
        return []
    found = _get_client(uid)
    return [found] if found else []


@app.get("/lobbies", response_class=HTMLResponse)
async def lobbies_page(request: Request) -> HTMLResponse:
    options = {"ALL": "All clients"}
    for c in app_state.clients:
        options[str(c.client_data.uid)] = f"{c.client_data.name} ({c.client_data.uid})"
    context = {
        "request": request,
        "theme": {
            "primary": PRIMARY_COLOR,
            "secondary": SECONDARY_COLOR,
            "tertiary": TERTIARY_COLOR,
            "background": BACKGROUND_COLOR,
            "surface": SURFACE_COLOR,
        },
        "target_options": options,
        "private_client": _active_private_client(),
    }
    return templates.TemplateResponse("lobbies.html", context)


def _active_private_client() -> Client | None:
    for client in app_state.clients:
        if client.private_search_list.entries:
            return client
    return app_state.clients[0] if app_state.clients else None


@app.post("/lobbies/join")
async def join_lobby(request: Request) -> RedirectResponse:
    form = await request.form()
    target = form.get("target")
    player_id = (form.get("player_id") or "").strip()
    lobby_name = (form.get("lobby_name") or "").strip()
    spectate = form.get("spectate") == "on"

    validate_error = None
    if player_id and lobby_name:
        validate_error = "Fill either Player ID or Lobby Name, not both."
    elif not player_id and not lobby_name:
        validate_error = "Provide a Player ID or Lobby Name."
    elif player_id and not player_id.isdigit():
        validate_error = "Player ID must be numeric."

    if validate_error:
        app_state.notify("Joiner", validate_error)
        return RedirectResponse(url="/lobbies", status_code=303)

    targets = _selected_clients(target)
    if not targets:
        app_state.notify("Joiner", "No clients available")
        return RedirectResponse(url="/lobbies", status_code=303)

    target_str = (
        "all clients"
        if len(targets) != 1
        else f"{targets[0].client_data.name} ({targets[0].client_data.uid})"
    )

    if player_id:
        pid = int(player_id)
        for client in targets:
            if not client.is_connected:
                app_state.notify("Joiner", f"{client.client_data.name} is not connected")
                continue
            if spectate:
                client.send_spectate_request(None, pid)
            else:
                client.send_enter_game_request(None, pid)
        app_state.notify("Joiner", f"Attempted by Player ID {player_id} on {target_str}")
    else:
        for client in targets:
            if not client.is_connected:
                app_state.notify("Joiner", f"{client.client_data.name} is not connected")
                continue
            if spectate:
                client.send_spectate_request(lobby_name, None)
            else:
                client.send_enter_game_request(lobby_name, None)
        app_state.notify("Joiner", f"Attempted lobby named '{lobby_name}' on {target_str}")

    return RedirectResponse(url="/lobbies", status_code=303)


@app.get("/general", response_class=HTMLResponse)
async def general_page(request: Request) -> HTMLResponse:
    general = app_state.states["general_settings"]
    context = {
        "request": request,
        "theme": {
            "primary": PRIMARY_COLOR,
            "secondary": SECONDARY_COLOR,
            "tertiary": TERTIARY_COLOR,
            "background": BACKGROUND_COLOR,
            "surface": SURFACE_COLOR,
        },
        "general": general,
    }
    return templates.TemplateResponse("general.html", context)


@app.post("/general/update")
async def general_update(request: Request) -> RedirectResponse:
    form = await request.form()
    general = app_state.states["general_settings"]
    general["detect_moderators"] = form.get("detect_moderators") == "on"
    general["trace_packets"] = form.get("trace_packets") == "on"
    autosave = form.get("auto_save_config") == "on"
    general["auto_save_config"] = autosave
    if autosave:
        save_config(app_state.states)
        app_state.notify("Config", "Saved automatically")
    return RedirectResponse(url="/general", status_code=303)


@app.get("/abuse", response_class=HTMLResponse)
async def abuse_page(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "theme": {
            "primary": PRIMARY_COLOR,
            "secondary": SECONDARY_COLOR,
            "tertiary": TERTIARY_COLOR,
            "background": BACKGROUND_COLOR,
            "surface": SURFACE_COLOR,
        },
    }
    return templates.TemplateResponse("abuse.html", context)


@app.post("/abuse/delete-account")
async def abuse_delete_account(request: Request) -> RedirectResponse:
    form = await request.form()
    token = (form.get("token") or "").strip()
    if not token:
        app_state.notify("Abuse", "Invalid sign-in token")
        return RedirectResponse(url="/abuse", status_code=303)
    response: dict[str, Any] | Exception = DeleteAccount(token).execute()
    if isinstance(response, Exception):
        app_state.notify("Abuse", f"Failed to delete account: {response}")
    elif response.get("Error"):
        app_state.notify("Abuse", f"Failed to delete account: {response['Error']}")
    else:
        app_state.notify("Abuse", "Account deleted")
    return RedirectResponse(url="/abuse", status_code=303)


@app.post("/abuse/send-plasma")
async def abuse_send_plasma(request: Request) -> RedirectResponse:
    form = await request.form()
    token = (form.get("token") or "").strip()
    target = (form.get("target") or "").strip()
    amount = (form.get("amount") or "").strip()
    if not token or not target.isdigit() or not amount.isdigit():
        app_state.notify("Abuse", "Provide token, numeric target, and numeric amount")
        return RedirectResponse(url="/abuse", status_code=303)
    response: dict[str, Any] | Exception = CoinPurchase(
        token, "GIVE_PLASMA", int(target), int(amount)
    ).execute()
    if isinstance(response, Exception):
        app_state.notify("Abuse", f"Failed to send plasma: {response}")
    elif response.get("Error"):
        app_state.notify("Abuse", f"Failed to send plasma: {response['Error']}")
    else:
        spent = response.get("CoinsSpent", 0)
        remaining = response.get("CoinsRemaining", 0)
        app_state.notify("API", f"Sent {spent} plasma to {target}. {remaining} remaining.")
    return RedirectResponse(url="/abuse", status_code=303)


@app.get("/bin", response_class=HTMLResponse)
async def bin_page(request: Request) -> HTMLResponse:
    text = app_state.states.get("bin_text", "")
    context = {
        "request": request,
        "theme": {
            "primary": PRIMARY_COLOR,
            "secondary": SECONDARY_COLOR,
            "tertiary": TERTIARY_COLOR,
            "background": BACKGROUND_COLOR,
            "surface": SURFACE_COLOR,
        },
        "text": text,
    }
    return templates.TemplateResponse("bin.html", context)


@app.post("/bin/save")
async def bin_save(request: Request) -> RedirectResponse:
    form = await request.form()
    app_state.states["bin_text"] = form.get("bin_text", "")
    save_config(app_state.states)
    app_state.notify("Bin", "Saved scratchpad")
    return RedirectResponse(url="/bin", status_code=303)


@app.get("/worlddbg", response_class=HTMLResponse)
async def worlddbg_page(request: Request) -> HTMLResponse:
    clients = app_state.clients
    context = {
        "request": request,
        "theme": {
            "primary": PRIMARY_COLOR,
            "secondary": SECONDARY_COLOR,
            "tertiary": TERTIARY_COLOR,
            "background": BACKGROUND_COLOR,
            "surface": SURFACE_COLOR,
        },
        "clients": clients,
    }
    return templates.TemplateResponse("worlddbg.html", context)


@app.get("/api/worlddbg/state")
async def worlddbg_state() -> JSONResponse:
    return JSONResponse(
        {"clients": [_client_world_snapshot(c) for c in app_state.clients]}
    )


def main() -> None:
    os.environ.setdefault("UVICORN_LOOP", "asyncio")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
