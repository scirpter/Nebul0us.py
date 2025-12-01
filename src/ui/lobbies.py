from __future__ import annotations

from collections.abc import Iterable
from nicegui import events, ui

from base.app import App
from game.models.client.client import Client
from ui.components.cards import glass_card


def render(app: App) -> None:
    with glass_card():
        ui.label("Join Lobby").classes("text-lg font-semibold text-slate-100")
        ui.label("Target a client (or all) and join by player ID or lobby name. Fill exactly one field.").classes(
            "text-sm text-slate-400"
        )

        with ui.row().classes("gap-4 flex-wrap"):
            target_select = ui.select(
                _build_target_options(app),
                value="ALL",
                label="Target client",
            ).classes("w-full md:w-80")

        with ui.row().classes("gap-4 flex-wrap"):
            player_id_input = ui.input(label="Player ID", placeholder="e.g. 123456").classes("w-full md:w-56")
            lobby_name_input = ui.input(label="Lobby Name", placeholder="e.g. My Lobby").classes("w-full md:w-56")

        with ui.row().classes("gap-3 flex-wrap"):
            join_button = ui.button(
                "Join",
                icon="login",
                on_click=lambda: _join(app, target_select, player_id_input, lobby_name_input, False),
            )
            spectate_button = ui.button(
                "Spectate",
                icon="visibility",
                on_click=lambda: _join(app, target_select, player_id_input, lobby_name_input, True),
            )
            ui.button(
                "Clear",
                icon="clear",
                on_click=lambda: _clear_inputs(player_id_input, lobby_name_input, helper_label, join_button, spectate_button),
            )

        helper_label = ui.label("").classes("text-sm text-amber-400")

    join_button.disable()
    spectate_button.disable()

    def validate(_: events.ValueChangeEventArguments | None = None) -> None:
        pid = (player_id_input.value or "").strip()
        name = (lobby_name_input.value or "").strip()

        if pid and name:
            helper_label.set_text("Fill either Player ID or Lobby Name, not both.")
            join_button.disable()
            spectate_button.disable()
            return
        if not pid and not name:
            helper_label.set_text("Provide a Player ID or Lobby Name.")
            join_button.disable()
            spectate_button.disable()
            return
        if pid and not pid.isdigit():
            helper_label.set_text("Player ID must be numeric.")
            join_button.disable()
            spectate_button.disable()
            return
        helper_label.set_text("")
        join_button.enable()
        spectate_button.enable()

    player_id_input.on_value_change(validate)
    lobby_name_input.on_value_change(validate)

    with glass_card():
        with ui.row().classes("justify-between items-center w-full"):
            ui.label("Private Games").classes("text-lg font-semibold text-slate-100")
            with ui.row().classes("gap-2 items-center"):
                ui.button("Prev", icon="chevron_left", on_click=lambda: _step_page(app, -1)).classes(
                    "bg-slate-800 text-slate-200"
                )
                ui.button("Next", icon="chevron_right", on_click=lambda: _step_page(app, 1)).classes(
                    "bg-slate-800 text-slate-200"
                )
                ui.button("Refresh", icon="refresh", on_click=lambda: _refresh_private_games(app)).classes(
                    "bg-slate-800 text-slate-200"
                )
        with ui.row().classes("gap-2 items-center"):
            ui.label("Current Page").classes("text-xs text-slate-500 uppercase tracking-[0.3em]")
            page_label = ui.label("-").classes("text-xs uppercase tracking-[0.35em] text-slate-500")
        entries_container = ui.column().classes("gap-3 w-full")

    def update_targets() -> None:
        target_select.options = _build_target_options(app)
        if target_select.value not in target_select.options:
            target_select.value = "ALL"
        target_select.update()

    def render_private_games() -> None:
        client = _active_private_client(app)
        entries_container.clear()
        if not app.clients or not client:
            page_label.set_text("-")
            with entries_container:
                ui.label("No private games data available.").classes("text-sm text-slate-500")
            return

        page_label.set_text(str(client.private_search_list.page))

        if not client.private_search_list.entries:
            with entries_container:
                ui.label("No lobbies on this page.").classes("text-sm text-slate-500")
            return

        for entry in client.private_search_list.entries:
            with entries_container:
                row = glass_card(padding="p-4", gap="gap-2")
                with row:
                    ui.label(entry.name).classes("text-base font-semibold text-slate-100")
                    ui.label(
                        f"{entry.players_in_lobby}/{entry.max_players} players • {getattr(entry.game_mode, 'name', entry.game_mode)}"
                    ).classes("text-xs text-slate-400 uppercase tracking-[0.3em]")
                    ui.button(
                        "Copy Name",
                        icon="content_copy",
                        on_click=lambda name=entry.name: _copy_private_name(app, name),
                    ).classes("bg-slate-800 text-slate-200 w-fit")

    def poll_private_games() -> None:
        render_private_games()

    refresh_handles = {
        "targets": update_targets,
        "private": poll_private_games,
    }

    ui.timer(2.0, refresh_handles["targets"])
    ui.timer(1.5, refresh_handles["private"])
    render_private_games()


def _build_target_options(app: App) -> dict[str, str]:
    options = {"ALL": "All clients"}
    for client in app.clients:
        options[str(client.client_data.uid)] = f"{client.client_data.name} ({client.client_data.uid})"
    return options


def _clear_inputs(
    player_input: ui.input,
    lobby_input: ui.input,
    helper_label: ui.label,
    join_button: ui.button,
    spectate_button: ui.button,
) -> None:
    player_input.value = ""
    lobby_input.value = ""
    helper_label.set_text("")
    join_button.disable()
    spectate_button.disable()


def _selected_clients(app: App, value: str | None) -> Iterable[Client]:
    if not app.clients:
        return []
    if not value or value == "ALL":
        return list(app.clients)
    try:
        uid = int(value)
    except (TypeError, ValueError):
        return []
    for client in app.clients:
        if client.client_data.uid == uid:
            return [client]
    return []


def _join(
    app: App,
    target_select: ui.select,
    player_input: ui.input,
    lobby_input: ui.input,
    spectate: bool,
) -> None:
    player_value = (player_input.value or "").strip()
    lobby_value = (lobby_input.value or "").strip()

    validate_error = None
    if player_value and lobby_value:
        validate_error = "Fill either Player ID or Lobby Name, not both."
    elif not player_value and not lobby_value:
        validate_error = "Provide a Player ID or Lobby Name."
    elif player_value and not player_value.isdigit():
        validate_error = "Player ID must be numeric."

    if validate_error:
        app.notify("Joiner", validate_error)
        return

    targets = list(_selected_clients(app, target_select.value))
    if not targets:
        app.notify("Joiner", "No clients available")
        return

    target_str = (
        "all clients"
        if len(targets) != 1
        else f"{targets[0].client_data.name} ({targets[0].client_data.uid})"
    )

    if player_value:
        player_id = int(player_value)
        for client in targets:
            if not client.is_connected:
                app.notify("Joiner", f"{client.client_data.name} is not connected")
                continue
            if spectate:
                client.send_spectate_request(None, player_id)
            else:
                client.send_enter_game_request(None, player_id)
        app.notify("Joiner", f"Attempted by Player ID {player_value} on {target_str}")
    elif lobby_value:
        for client in targets:
            if not client.is_connected:
                app.notify("Joiner", f"{client.client_data.name} is not connected")
                continue
            if spectate:
                client.send_spectate_request(lobby_value, None)
            else:
                client.send_enter_game_request(lobby_value, None)
        app.notify("Joiner", f"Attempted lobby named '{lobby_value}' on {target_str}")


def _active_private_client(app: App) -> Client | None:
    for client in app.clients:
        if client.private_search_list.entries:
            return client
    return app.clients[0] if app.clients else None


def _step_page(app: App, delta: int) -> None:
    client = _active_private_client(app)
    if not client:
        return
    client.private_search_list.page = max(0, client.private_search_list.page + delta)
    client.request_private_search_list()


def _refresh_private_games(app: App) -> None:
    client = _active_private_client(app)
    if client:
        client.request_private_search_list()


def _copy_private_name(app: App, name: str) -> None:
    ui.run_javascript(f"navigator.clipboard.writeText({name!r});")
    app.notify("Private Games", f"Copied lobby name: {name}")
