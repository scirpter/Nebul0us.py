from __future__ import annotations

from uuid import uuid4

from nicegui import events, ui

from base.app import App, DevLogEntry
from ui.components.cards import glass_card


SEVERITY_OPTIONS: dict[str, str] = {
    "info": "Info",
    "warning": "Warning",
    "error": "Error",
}


def render(app: App) -> None:
    container_id = f"devlog-container-{uuid4().hex}"

    with glass_card():
        ui.label("Developer Logs").classes("text-lg font-semibold text-slate-100")
        ui.label(
            "Live console of events emitted by the app. Filter by severity or search keywords."
        ).classes("text-sm text-slate-400")

        with ui.row().classes("gap-4 flex-wrap"):
            search_input = ui.input(
                placeholder="Search logs…",
                label="Search",
            ).classes("w-full md:w-80")

            severity_select = ui.select(
                SEVERITY_OPTIONS,
                value=list(SEVERITY_OPTIONS.keys()),
                label="Severity",
                multiple=True,
            ).classes("w-full md:w-64")

            auto_scroll = ui.switch("Auto-scroll", value=True)
            pause_ingest = ui.switch("Pause stream", value=False)

        controls = ui.row().classes("gap-3 flex-wrap")
        with controls:
            ui.button("Copy", icon="content_copy", on_click=lambda: _copy_filtered(app, search_input, severity_select)).classes(
                "bg-slate-800 text-slate-200"
            )
            ui.button("Clear", icon="delete", on_click=lambda: _clear_logs(app, log_container)).classes(
                "bg-rose-500/80 text-slate-100"
            )

        log_container = ui.column().classes(
            "w-full max-h-[65vh] overflow-y-auto pr-2 gap-3"
        )
        log_container.props(f'id="{container_id}"')

    def rebuild() -> None:
        log_container.clear()
        filtered = _filtered_entries(app, search_input.value, severity_select.value)
        if not filtered:
            with log_container:
                ui.label("No logs yet.").classes("italic text-slate-500")
            return
        for entry in filtered:
            _render_entry(entry)

    def _render_entry(entry: DevLogEntry) -> None:
        severity_color = {
            "info": "text-slate-300",
            "warning": "text-amber-300",
            "error": "text-rose-300",
        }.get(entry.importance, "text-rose-300")
        with log_container:
            with ui.element("div").classes(
                "flex gap-4 items-start bg-slate-900/60 border border-slate-700/40 "
                "rounded-xl px-4 py-3 backdrop-blur-md shadow-sm"
            ):
                ui.label(entry.timestamp.strftime("%d/%m/%Y %H:%M:%S")).classes(
                    "text-xs text-slate-500 w-36 shrink-0"
                )
                ui.label(entry.message).classes(f"text-sm leading-relaxed {severity_color}")

    rebuild()

    def poll_queue() -> None:
        if pause_ingest.value:
            return
        updated = False
        while not app.devlog_queue.empty():
            entry = app.devlog_queue.get()
            if entry not in app.devlog_entries:
                app.devlog_entries.append(entry)
            if _matches_filters(entry, search_input.value, severity_select.value):
                _render_entry(entry)
                updated = True
        if updated and auto_scroll.value:
            ui.run_javascript(
                f"const el=document.getElementById('{container_id}');"
                "if(el){el.scrollTo({top:el.scrollHeight, behavior:'smooth'});}"
            )

    def on_filter_change(_: events.ValueChangeEventArguments) -> None:
        rebuild()

    search_input.on_value_change(on_filter_change)
    severity_select.on_value_change(on_filter_change)

    ui.timer(0.5, poll_queue)


def _filtered_entries(app: App, query: str | None, severities: list[str] | None) -> list[DevLogEntry]:
    entries = app.devlog_entries
    if severities:
        entries = [entry for entry in entries if entry.importance in severities]
    if query:
        lowered = query.lower()
        entries = [
            entry for entry in entries if lowered in entry.message.lower()
        ]
    return entries


def _matches_filters(entry: DevLogEntry, query: str | None, severities: list[str] | None) -> bool:
    if severities and entry.importance not in severities:
        return False
    if query and query.lower() not in entry.message.lower():
        return False
    return True


def _copy_filtered(app: App, search_input: ui.input, severity_select: ui.select) -> None:
    filtered = _filtered_entries(app, search_input.value, severity_select.value)
    if not filtered:
        ui.notify("No logs to copy", type="warning")
        return
    lines = [
        f"[{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {entry.importance.upper()}: {entry.message}"
        for entry in filtered
    ]
    text = "\n".join(lines)
    ui.run_javascript(f"navigator.clipboard.writeText({text!r});")
    ui.notify("Copied logs to clipboard", type="info")


def _clear_logs(app: App, container: ui.column) -> None:
    app.devlog_entries.clear()
    while not app.devlog_queue.empty():
        app.devlog_queue.get()
    container.clear()
    with container:
        ui.label("No logs yet.").classes("italic text-slate-500")
