from __future__ import annotations
from typing import Literal
import flet as ft
from datetime import datetime

from base.app import App


LogImportance = Literal["info", "warning", "error"]


class DevLog:
    def __init__(self, msg: str, importance: LogImportance) -> None:
        self.msg: str = msg
        self.ts: datetime = datetime.now()
        self.importance: LogImportance = importance


class DevLogsTab(ft.Tab):
    _instance: DevLogsTab | None = None

    def __init__(self, app: App) -> None:
        DevLogsTab._instance: DevLogsTab | None = self
        self.logs: list[DevLog] = []
        super().__init__(
            text="Dev Logs",
            content=ft.Column(controls=[ft.Text("No logs yet. Do stuff")]),
        )

    @staticmethod
    def log(msg: str, importance: LogImportance) -> None:
        self: None | DevLogsTab = DevLogsTab._instance
        self.logs.append(DevLog(msg, importance))
        self.content = ft.Container(
            ft.Column(
                controls=[
                    ft.Row(
                        [
                            ft.Text(log.ts.strftime("%H:%M:%S"), color=ft.colors.GREY),
                            ft.Text(
                                log.msg,
                                color=(
                                    ft.colors.GREY
                                    if log.importance == "info"
                                    else (
                                        ft.colors.YELLOW
                                        if log.importance == "warning"
                                        else ft.colors.RED
                                    )
                                ),
                            ),
                        ]
                    )
                    for log in reversed(self.logs)
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ),
            margin=ft.Margin(0, 10, 0, 0),
        )
        self.update()
