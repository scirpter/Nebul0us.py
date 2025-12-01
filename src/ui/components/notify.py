from __future__ import annotations
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from time import monotonic
from typing import Callable

from nicegui import ui


class NotificationKind(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass(slots=True)
class Toast:
    title: str
    message: str
    kind: NotificationKind
    created_at: float


class NotificationManager:
    def __init__(self, limit: int = 5, duration_seconds: float = 7.0) -> None:
        self.limit = limit
        self.duration_seconds = duration_seconds
        self.active: deque[Toast] = deque()
        self.history: list[Toast] = []
        self.container: ui.column | None = None
        self._timer = None

    def mount(self) -> None:
        self.container = ui.column().classes(
            "fixed top-6 right-6 z-50 gap-3 max-h-[70vh] overflow-y-auto pr-2 pointer-events-none"
        )
        self._render()

    def push(self, title: str, message: str, *, kind: NotificationKind = NotificationKind.INFO) -> None:
        toast = Toast(title=title, message=message, kind=kind, created_at=monotonic())
        self.active.appendleft(toast)
        self.history.append(toast)
        while len(self.active) > self.limit:
            self.active.pop()
        self._render()
        # schedule one-shot expiry per toast
        ui.timer(self.duration_seconds, lambda t=toast: self._expire(t), once=True)

    def _render(self) -> None:
        if not self.container:
            return

        palette = {
            NotificationKind.INFO: ("bg-slate-900/80", "border-slate-500/70", "text-slate-50", "info"),
            NotificationKind.SUCCESS: ("bg-emerald-400/18", "border-emerald-300/60", "text-emerald-50", "check_circle"),
            NotificationKind.WARNING: ("bg-amber-400/18", "border-amber-300/60", "text-amber-50", "warning_amber"),
            NotificationKind.ERROR: ("bg-rose-400/20", "border-rose-300/60", "text-rose-50", "error"),
        }
        self.container.clear()
        for toast in self.active:
            bg, border, text_color, icon = palette[toast.kind]
            with self.container:
                with ui.card().classes(
                    f"toast-card frosted-card {bg} {border} {text_color} border shadow-xl rounded-xl "
                    "backdrop-blur-xl w-80 pointer-events-auto animate-slide-in"
                ):
                    with ui.row().classes("items-start gap-3"):
                        ui.icon(icon).classes("text-base opacity-80")
                        with ui.column().classes("gap-1"):
                            ui.label(toast.title).classes("text-sm font-semibold")
                            ui.label(toast.message).classes("text-xs opacity-80")
                        ui.button(icon="close", on_click=lambda t=toast: self._expire(t)).props(
                            "round dense flat"
                        ).classes("text-slate-400 hover:text-slate-100")
                    ui.element("div").classes("toast-progress").style(
                        f"--toast-duration:{self.duration_seconds}s"
                    )

    def _expire(self, toast: Toast) -> None:
        try:
            self.active.remove(toast)
        except ValueError:
            return
        self._render()


def wrap_app_notify(app_notify: Callable[[str, str], None], manager: NotificationManager) -> Callable[[str, str], None]:
    def wrapped(title: str, message: str) -> None:
        manager.push(title, message)
        app_notify(title, message)

    return wrapped
