from __future__ import annotations

from nicegui import events, ui

from base.app import App
from helpers.config_integrity import save_config
from ui.components.cards import glass_card


def render(app: App) -> None:
    general = app.states["general_settings"]

    with glass_card():
        ui.label("General Settings").classes(
            "text-lg font-semibold text-slate-100"
        )
        ui.label(
            "Toggles that affect global behavior of the client. Changes persist automatically when enabled."
        ).classes("text-sm text-slate-400")

        with ui.row().classes("gap-4 flex-wrap"):
            detect_toggle = ui.switch(
                "Detect Moderators",
                value=general.get("detect_moderators", False),
            )
            trace_toggle = ui.switch(
                "Trace Packets",
                value=general.get("trace_packets", False),
            )
            autosave_toggle = ui.switch(
                "Auto-save Config",
                value=general.get("auto_save_config", True),
            )

        helper_label = ui.label("").classes(
            "text-xs text-slate-500 uppercase tracking-[0.3em]"
        )

        def on_detect_change(_: events.ValueChangeEventArguments) -> None:
            general["detect_moderators"] = bool(detect_toggle.value)

        def on_trace_change(_: events.ValueChangeEventArguments) -> None:
            general["trace_packets"] = bool(trace_toggle.value)

        def on_autosave_change(_: events.ValueChangeEventArguments) -> None:
            general["auto_save_config"] = bool(autosave_toggle.value)
            helper_label.set_text(
                "Auto-save enabled"
                if autosave_toggle.value
                else "Auto-save disabled"
            )

        detect_toggle.on_value_change(on_detect_change)
        trace_toggle.on_value_change(on_trace_change)
        autosave_toggle.on_value_change(on_autosave_change)

        def manual_save() -> None:
            if autosave_toggle.value:
                app.notify(
                    "Config", "Auto-save is enabled. Manual save not required."
                )
                return
            save_config(app.states)
            app.notify("Config", "Configuration saved")

        ui.button("Save Config", icon="save", on_click=manual_save).classes(
            "bg-slate-800 text-slate-200 w-fit"
        )

    snapshot = {"value": repr(app.states)}

    def maybe_save() -> None:
        if not autosave_toggle.value:
            if general.get("auto_save_config"):
                general["auto_save_config"] = False
            return
        if not general.get("auto_save_config"):
            general["auto_save_config"] = True
        current = repr(app.states)
        if current != snapshot["value"]:
            snapshot["value"] = current
            save_config(app.states)
            helper_label.set_text("Last saved automatically")

    ui.timer(1.0, maybe_save)
