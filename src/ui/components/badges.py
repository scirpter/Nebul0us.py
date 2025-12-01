from __future__ import annotations

from nicegui import ui


def status_badge(label: str, *, kind: str = "default") -> ui.label:
    color_map = {
        "default": "bg-slate-700/70 text-slate-200 border border-slate-600/60",
        "success": "bg-emerald-500/20 text-emerald-300 border border-emerald-400/40",
        "warning": "bg-amber-500/20 text-amber-300 border border-amber-400/40",
        "danger": "bg-rose-500/20 text-rose-300 border border-rose-400/40",
        "info": "bg-cyan-500/20 text-cyan-300 border border-cyan-400/40",
    }
    return ui.label(label).classes(
        f"px-2 py-1 rounded-full text-xs font-semibold tracking-wide uppercase "
        f"{color_map.get(kind, color_map['default'])}"
    )
