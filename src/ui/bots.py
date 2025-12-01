from __future__ import annotations

from typing import Callable

from nicegui import events, ui

from base.app import App
from game.enums import REGION
from game.enums.game_mode import GAME_MODE
from game.models.client.client import Client
from ui.components.badges import status_badge
from ui.components.cards import glass_card


def render(app: App) -> None:
    status_updaters: list[Callable[[], None]] = []

    header = ui.row().classes("justify-between items-center w-full")
    with header:
        titles = ui.column().classes("gap-1")
        with titles:
            ui.label("Bot Fleet").classes("text-2xl font-semibold text-slate-100")
            summary_label = ui.label("").classes("text-sm text-slate-400")
        actions = ui.row().classes("gap-3 items-center")
        with actions:
            ui.button("Add Bot", icon="add", on_click=lambda: _open_add_bot_dialog(app, refresh)).classes(
                "bg-violet-500/80 hover:bg-violet-400 text-slate-100"
            )
            ui.button("Disconnect All", icon="power_settings_new", on_click=lambda: _disconnect_all(app, refresh)).classes(
                "bg-slate-800 hover:bg-slate-700 text-slate-200"
            )

    cards_container = ui.element("div").classes(
        "grid grid-cols-1 gap-6 w-full xl:grid-cols-2 2xl:grid-cols-3"
    )

    def update_summary() -> None:
        total = len(app.clients)
        connected = sum(1 for client in app.clients if client.is_connected)
        summary_label.set_text(f"{connected} / {total} connected")

    def refresh() -> None:
        cards_container.clear()
        status_updaters.clear()
        if not app.clients:
            with cards_container:
                card = glass_card()
                with card:
                    ui.label("No bots configured yet.").classes("text-sm text-slate-400")
            update_summary()
            return

        for client in app.clients:
            _build_bot_card(app, client, cards_container, status_updaters, refresh)
        update_summary()

    refresh()
    ui.timer(1.0, lambda: [_update() for _update in status_updaters])


def _build_bot_card(
    app: App,
    client: Client,
    container: ui.element,
    status_updaters: list[Callable[[], None]],
    refresh_callback: Callable[[], None],
) -> None:
    regions = REGION.all()
    modes = GAME_MODE.all()

    with container:
        card = glass_card()
        with card:
            header = ui.row().classes("justify-between items-start")
            with header:
                meta = ui.column().classes("gap-1")
                with meta:
                    ui.label(client.client_data.name).classes("text-xl font-semibold text-slate-100")
                    ui.label(f"UID {client.client_data.uid}").classes("text-xs uppercase tracking-[0.3em] text-slate-500")
                status_chip = status_badge("Offline", kind="danger")

            def update_status() -> None:
                if client.is_connected:
                    status_chip.set_text("Connected")
                    status_chip.classes(
                        replace="px-2 py-1 rounded-full text-xs font-semibold tracking-wide uppercase "
                        "bg-emerald-500/20 text-emerald-200 border border-emerald-400/40"
                    )
                else:
                    status_chip.set_text("Offline")
                    status_chip.classes(
                        replace="px-2 py-1 rounded-full text-xs font-semibold tracking-wide uppercase "
                        "bg-rose-500/25 text-rose-200 border border-rose-400/50"
                    )

            update_status()
            status_updaters.append(update_status)

            with ui.element("div").classes("grid grid-cols-1 lg:grid-cols-2 gap-4 w-full"):
                region_value = getattr(client.client_data, "server_region", None) or REGION.EU.name
                stored_mode = client.settings.get("game_mode", GAME_MODE.FFA_ULTRA.name)
                region_select = ui.select(
                    regions,
                    value=region_value,
                    label="Region",
                ).classes("w-full")
                mode_select = ui.select(
                    modes,
                    value=stored_mode,
                    label="Game Mode",
                ).classes("w-full")

            with ui.row().classes("gap-4 flex-wrap items-center"):
                mayhem_toggle = ui.switch("Mayhem", value=False)
                private_toggle = ui.switch("Private Search", value=False)
                auto_respawn_toggle = ui.switch(
                    "Auto Respawn", value=client.options_data.auto_respawn
                )
                chase_toggle = ui.switch(
                    "Chase Closest Holes", value=client.options_data.chase_nearest_holes
                )

            with ui.column().classes("gap-4"):
                active_label = ui.label("").classes("text-xs text-slate-400 uppercase tracking-[0.3em]")
                active_slider = ui.slider(min=20, max=600, value=client.settings["active_keep_alive_ms"])
                idle_label = ui.label("").classes("text-xs text-slate-400 uppercase tracking-[0.3em]")
                idle_slider = ui.slider(min=200, max=1200, value=client.settings["idle_keep_alive_ms"])

            def sync_keep_alive_labels() -> None:
                active_label.set_text(f"Active Keep Alive â€¢ {client.settings['active_keep_alive_ms']} ms")
                idle_label.set_text(f"Idle Keep Alive â€¢ {client.settings['idle_keep_alive_ms']} ms")

            sync_keep_alive_labels()

            with ui.row().classes("gap-3 flex-wrap"):
                name_input = ui.input(label="Bot Name", value=client.client_data.name).classes("flex-1")
                ui.button(
                    "Apply Name",
                    icon="check",
                    on_click=lambda: _rename_bot(app, client, name_input.value or "", refresh_callback),
                ).classes("bg-emerald-500/80 hover:bg-emerald-400 text-slate-900")

            with ui.row().classes("gap-3 flex-wrap"):
                ui.button(
                    "Start Playing",
                    icon="play_arrow",
                    on_click=lambda: _start_playing(app, client),
                ).classes("bg-emerald-500/80 hover:bg-emerald-400 text-slate-900")
                ui.button(
                    "Connect",
                    icon="bolt",
                    on_click=lambda: _connect_bot(
                        app,
                        client,
                        region_select.value,
                        mode_select.value,
                        bool(mayhem_toggle.value),
                        bool(private_toggle.value),
                    ),
                ).classes("bg-cyan-500/80 hover:bg-cyan-400 text-slate-900")
                ui.button(
                    "Disconnect",
                    icon="link_off",
                    on_click=lambda: _disconnect_bot(app, client),
                ).classes("bg-slate-800 hover:bg-slate-700 text-slate-200")
                ui.button(
                    "Copy Token",
                    icon="content_copy",
                    on_click=lambda: _copy_ticket(app, client),
                ).classes("bg-slate-800 hover:bg-slate-700 text-slate-200")
                ui.button(
                    "Delete",
                    icon="delete",
                    on_click=lambda: _delete_bot(app, client, refresh_callback),
                ).classes("bg-rose-500/80 hover:bg-rose-500 text-slate-100")

            def on_autorespawn_change(_: events.ValueChangeEventArguments) -> None:
                client.options_data.auto_respawn = bool(auto_respawn_toggle.value)

            def on_chase_change(_: events.ValueChangeEventArguments) -> None:
                client.options_data.chase_nearest_holes = bool(chase_toggle.value)

            def on_active_change(e: events.ValueChangeEventArguments) -> None:
                client.settings["active_keep_alive_ms"] = int(e.value)
                sync_keep_alive_labels()

            def on_idle_change(e: events.ValueChangeEventArguments) -> None:
                client.settings["idle_keep_alive_ms"] = int(e.value)
                sync_keep_alive_labels()

            auto_respawn_toggle.on_value_change(on_autorespawn_change)
            chase_toggle.on_value_change(on_chase_change)
            active_slider.on_value_change(on_active_change)
            idle_slider.on_value_change(on_idle_change)


def _rename_bot(app: App, client: Client, name: str, refresh_callback: Callable[[], None]) -> None:
    name = name.strip()
    if not name:
        app.notify("Session", "Bot name can't be empty")
        return
    if len(name) > 12:
        app.notify("Session", "Bot name can't be longer than 12 characters")
        return
    if any(
        other.client_data.name == name and other is not client
        for other in app.clients
    ):
        app.notify("Session", "Bot with this name already exists")
        return
    if name == client.client_data.name:
        app.notify("Session", "No changes made")
        return

    client.client_data.name = name
    client.settings["player_name"] = name
    app.notify("Session", f"Renamed bot to {name}")
    refresh_callback()


def _connect_bot(
    app: App,
    client: Client,
    region: str | None,
    mode: str | None,
    mayhem: bool,
    private_search: bool,
) -> None:
    if client.is_connected:
        app.notify("Session", "Bot is already connected")
        return
    if not region:
        app.notify("Session", "Select a region before connecting")
        return

    selected_mode = GAME_MODE.from_string(mode or GAME_MODE.FFA_ULTRA.name)
    client.settings["game_mode"] = selected_mode.name

    result = client.connect(
        region=region,
        game_mode=selected_mode,
        connect_in_private_search=private_search,
        mayhem=mayhem,
    )
    if isinstance(result, Exception):
        app.notify("Connection Error", str(result))
    else:
        app.notify("Session", f"Connecting {client.client_data.name}...")


def _disconnect_bot(app: App, client: Client) -> None:
    if not client.is_connected:
        app.notify("Session", "Bot is not connected")
        return
    client.disconnect()
    app.notify("Session", f"{client.client_data.name} disconnected")


def _start_playing(app: App, client: Client) -> None:
    if not client.is_connected:
        app.notify("Session", f"{client.client_data.name} is not connected")
        return
    client.start_playing()
    app.notify("Player", f"{client.client_data.name} sent play request")


def _copy_ticket(app: App, client: Client) -> None:
    ticket = client.client_data.login_ticket or ""
    ui.run_javascript(f"navigator.clipboard.writeText({ticket!r});")
    app.notify("Info", "Copied bot ticket to clipboard")


def _delete_bot(app: App, client: Client, refresh_callback: Callable[[], None]) -> None:
    try:
        app.clients.remove(client)
    except ValueError:
        app.notify("Session", "Bot already removed")
        return

    for setting in list(app.states["client_settings"]):
        if setting["client_uid"] == client.client_data.uid:
            app.states["client_settings"].remove(setting)
            break

    app.notify("Session", f"Deleted {client.client_data.name}")
    refresh_callback()


def _disconnect_all(app: App, refresh_callback: Callable[[], None]) -> None:
    for client in app.clients:
        if client.is_connected:
            client.disconnect()
    app.notify("Session", "Disconnected all bots")
    refresh_callback()


def _open_add_bot_dialog(app: App, refresh_callback: Callable[[], None]) -> None:
    with ui.dialog() as dialog, ui.card().classes("bg-slate-950/80 border border-slate-800/60 p-6 w-[420px]"):
        ui.label("Add Bot").classes("text-lg font-semibold text-slate-100")
        ui.label(
            "Running more than four clients will require proxies or VPN. Max four per IP."
        ).classes("text-xs text-amber-300")
        name_input = ui.input(label="Bot Name").classes("w-full")
        ticket_input = ui.input(label="Bot Ticket", password=True).classes("w-full")

        def confirm() -> None:
            name = (name_input.value or "").strip()
            ticket = (ticket_input.value or "").strip()
            if not name:
                app.notify("Session", "Bot name can't be empty")
                return
            if not ticket:
                app.notify("Session", "Bot ticket can't be empty")
                return
            if any(client.client_data.name == name for client in app.clients):
                app.notify("Failure", f"Bot named {name} already exists")
                return
            if any(client.client_data.login_ticket == ticket for client in app.clients):
                app.notify("Failure", "Bot with this ticket already exists")
                return
            if not ticket.endswith("=") or "," not in ticket:
                app.notify("Failure", "Invalid ticket format")
                return
            account_id = ticket.split(",")[0]
            if not account_id.isdigit():
                app.notify("Failure", "Invalid ticket format")
                return

            dialog.close()
            client = Client(app, int(account_id), name, ticket)
            app.clients.append(client)
            client.setup_loops()
            app.notify("Session", f"Added {client.client_data.name}")
            refresh_callback()

        with ui.row().classes("justify-end gap-2 w-full mt-4"):
            ui.button("Cancel", on_click=dialog.close).classes("bg-slate-800 text-slate-200")
            ui.button("Add", on_click=confirm).classes("bg-violet-500 hover:bg-violet-400 text-slate-900")

    dialog.open()



