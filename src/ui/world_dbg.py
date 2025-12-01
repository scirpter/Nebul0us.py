from __future__ import annotations

from nicegui import events, ui

from base.app import App
from game.models.client.client import Client
from ui.components.cards import glass_card


def render(app: App) -> None:
    with glass_card():
        ui.label("World Debugger").classes("text-lg font-semibold text-slate-100")
        ui.label(
            "Inspect live world state for a connected client. Pause auto refresh to review historical data."
        ).classes("text-sm text-slate-400")

        with ui.row().classes("gap-4 flex-wrap"):
            client_select = ui.select(
                _client_options(app),
                value=_default_client_value(app),
                label="Client",
            ).classes("w-full md:w-64")
            view_select = ui.select(
                {"players": "Players", "holes": "Holes"},
                value="players",
                label="View",
            ).classes("w-full md:w-40")

        with ui.row().classes("gap-3 items-center flex-wrap"):
            ui.button(
                "Refresh",
                icon="refresh",
                on_click=lambda: _refresh_table(app, client_select, view_select, table, last_refresh_label),
            ).classes("bg-slate-800 text-slate-200")
            auto_switch = ui.switch("Auto Refresh", value=True)
            with ui.row().classes("items-center gap-2"):
                ui.label("Last Refresh").classes("text-xs text-slate-500 uppercase tracking-[0.3em]")
                last_refresh_label = ui.label("Never").classes("text-xs text-slate-500 uppercase tracking-[0.3em]")

        table = ui.table(columns=[], rows=[]).classes(
            "w-full bg-slate-950/70 border border-slate-800 text-slate-200 rounded-xl"
        )
        table.props('flat square dense wrap-cells separator="horizontal" hide-bottom-border')

    def periodic_refresh() -> None:
        if auto_switch.value:
            _refresh_table(app, client_select, view_select, table, last_refresh_label)

    ui.timer(1.2, periodic_refresh)

    def on_change(_: events.ValueChangeEventArguments) -> None:
        _refresh_table(app, client_select, view_select, table, last_refresh_label)

    client_select.on_value_change(on_change)
    view_select.on_value_change(on_change)

    def refresh_options() -> None:
        client_select.options = _client_options(app)
        client_select.update()

    ui.timer(2.5, refresh_options)
    _refresh_table(app, client_select, view_select, table, last_refresh_label)


def _client_options(app: App) -> dict[str, str]:
    return {
        str(client.client_data.uid): f"{client.client_data.name} ({client.client_data.uid})"
        for client in app.clients
    }


def _default_client_value(app: App) -> str | None:
    return str(app.clients[0].client_data.uid) if app.clients else None


def _selected_client(app: App, client_select: ui.select) -> Client | None:
    if not client_select.value:
        return None
    try:
        uid = int(client_select.value)
    except (TypeError, ValueError):
        return None
    for client in app.clients:
        if client.client_data.uid == uid:
            return client
    return None


def _refresh_table(
    app: App,
    client_select: ui.select,
    view_select: ui.select,
    table: ui.table,
    last_refresh_label: ui.label,
) -> None:
    client = _selected_client(app, client_select)
    if not client or not client.client_data.world:
        table.columns = []
        table.rows = [{"id": "-", "message": "Pick a client to view world data"}]
        table.props('no-data-label="No data available."')
        last_refresh_label.set_text("No data")
        table.update()
        return

    world = client.client_data.world
    view = view_select.value or "players"

    if view == "holes":
        columns = [
            {"name": "id", "label": "ID", "field": "id"},
            {"name": "type", "label": "Type", "field": "type"},
            {"name": "mass", "label": "Mass", "field": "mass"},
            {"name": "x", "label": "X", "field": "x"},
            {"name": "y", "label": "Y", "field": "y"},
        ]
        rows = [
            {
                "id": hid,
                "type": getattr(hole.type, "name", str(hole.type)),
                "mass": f"{hole.mass:.1f}",
                "x": f"{hole.pos.x:.1f}",
                "y": f"{hole.pos.y:.1f}",
            }
            for hid, hole in world.holes.copy().items()
        ]
    else:
        columns = [
            {"name": "id", "label": "ID", "field": "id"},
            {"name": "name", "label": "Name", "field": "name"},
            {"name": "mass", "label": "Mass", "field": "mass"},
            {"name": "blobs", "label": "Blobs", "field": "blobs"},
            {"name": "avg_x", "label": "Avg X", "field": "avg_x"},
            {"name": "avg_y", "label": "Avg Y", "field": "avg_y"},
        ]
        rows = []
        for pid, player in world.players.copy().items():
            average = player.get_avg_pos()
            rows.append(
                {
                    "id": pid,
                    "name": player.name,
                    "mass": f"{player.get_mass():.1f}",
                    "blobs": len(player.blobs),
                    "avg_x": f"{average.x:.1f}" if average else "-",
                    "avg_y": f"{average.y:.1f}" if average else "-",
                }
            )

    table.columns = columns
    table.rows = rows
    table.update()
    last_refresh_label.set_text("Just now")
