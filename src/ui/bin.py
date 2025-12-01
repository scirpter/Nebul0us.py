from __future__ import annotations

from nicegui import events, ui

from base.app import App
from ui.components.cards import glass_card


def render(app: App) -> None:
    with glass_card():
        ui.label("Scratchpad").classes("text-lg font-semibold text-slate-100")
        ui.label("A simple space to stash temporary notes. Content persists with the rest of your config.").classes(
            "text-sm text-slate-400"
        )

        def on_change(event: events.ValueChangeEventArguments) -> None:
            app.states["bin_text"] = event.value or ""

        ui.textarea(
            value=app.states.get("bin_text", ""),
            on_change=on_change,
            placeholder="Write something here that you need to save for later.",
        ).classes(
            "w-full min-h-[320px] bg-slate-950/70 border border-slate-800 rounded-xl text-slate-200"
        ).props("autogrow")
