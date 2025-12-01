from __future__ import annotations

from typing import Any

from nicegui import ui


def data_table(*, columns: list[dict[str, Any]], rows: list[dict[str, Any]], dense: bool = True) -> ui.table:
    table = ui.table(columns=columns, rows=rows, row_key="id").classes(
        "w-full frosted-card bg-slate-950/60 border border-slate-800 text-slate-200 rounded-2xl shadow-xl"
    )
    table.props(
        "flat square wrap-cells"
        + (" dense" if dense else "")
        + ' separator="horizontal" grid-lines hide-bottom-border'
    )
    return table
