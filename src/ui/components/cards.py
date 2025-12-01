from __future__ import annotations

from nicegui import ui


def glass_card(*, padding: str = "p-6", gap: str = "gap-4") -> ui.element:
    return ui.card().classes(
        "w-full frosted-card backdrop-blur-xl border border-slate-700/60 shadow-xl "
        "rounded-2xl transition-all duration-200 hover:border-slate-500/70 hover:-translate-y-[1px] "
        f"{padding} {gap}"
    )


def section(title: str, *, description: str | None = None) -> ui.element:
    column = ui.column().classes("gap-3 w-full")
    with column:
        with ui.row().classes("items-center gap-3"):
            ui.element("span").classes("h-[1px] w-6 accent-line rounded-full")
            ui.label(title).classes("text-lg font-semibold text-slate-100 tracking-wide")
        if description:
            ui.label(description).classes("text-sm text-slate-400 leading-relaxed")
    return column
