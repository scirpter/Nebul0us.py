from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable
from typing import Callable

from nicegui import ui

from .badges import status_badge


@dataclass(slots=True)
class ShellTab:
    label: str
    icon: str
    builder: Callable[[], None]



class AppShell:
    def __init__(
        self,
        *,
        title: str,
        subtitle: str,
        tabs: list[ShellTab],
        actions: Iterable[tuple[str, Callable[[], None]]] | None = None,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.tabs = tabs
        self.actions = list(actions or [])
        self.tab_refs: list[ui.tab] = []
        self.tabs_control: ui.tabs | None = None

    def build(self) -> None:
        with ui.element("div").classes("page-shell-background w-full"):
            with ui.column().classes(
                "w-full max-w-7xl mx-auto px-6 lg:px-10 py-10 box-border gap-8"
            ):
                self._build_header()
                self._build_tabs()

    def _build_header(self) -> None:
        with ui.element("div").classes(
            "frosted-card border border-slate-700/50 rounded-3xl p-6 shadow-2xl w-full"
        ):
            with ui.row().classes("justify-between items-start w-full gap-6 flex-wrap"):
                with ui.column().classes("gap-2 max-w-2xl"):
                    ui.label(self.title).classes(
                        "heading text-4xl font-extrabold tracking-tight text-glow accent-gradient-text bg-clip-text"
                    )
                    ui.label(self.subtitle).classes(
                        "text-sm uppercase tracking-[0.35em] text-slate-400"
                    )
                    ui.label(
                        "Live operations cockpit for Nebulous.io bots. Navigate fast, monitor clearly, and act confidently."
                    ).classes("text-sm text-slate-400 leading-relaxed")
                with ui.column().classes("items-end gap-3 min-w-[220px]"):
                    with ui.row().classes("gap-2 flex-wrap justify-end"):
                        status_badge("Alpha", kind="info")
                        status_badge("Dark Mode", kind="success")
                    if self.actions:
                        with ui.row().classes("gap-2 flex-wrap justify-end"):
                            for label, handler in self.actions:
                                ui.button(label, on_click=handler).classes(
                                    "pill-button text-slate-100 text-sm font-semibold"
                                )

    def _build_tabs(self) -> None:
        with ui.tabs().classes(
            "nav-tabs w-full backdrop-blur-md rounded-2xl px-2 py-1 shadow-xl text-slate-100"
        ) as tabs_control:
            self.tabs_control = tabs_control
            self.tab_refs = [
                ui.tab(tab.label, icon=tab.icon)
                for tab in self.tabs
            ]

        with ui.tab_panels(tabs_control, value=self.tab_refs[0]).classes(
            "tab-panels w-full rounded-3xl px-8 py-8 shadow-2xl min-h-[68vh]"
        ):
            for tab_ref, tab in zip(self.tab_refs, self.tabs, strict=True):
                with ui.tab_panel(tab_ref):
                    with ui.column().classes("w-full max-w-7xl mx-auto gap-6"):
                        tab.builder()

    def activate(self, label: str) -> None:
        if not self.tabs_control:
            return
        for ref, tab in zip(self.tab_refs, self.tabs, strict=True):
            if tab.label == label:
                self.tabs_control.value = ref
                self.tabs_control.update()
                break
