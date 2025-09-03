from __future__ import annotations
import flet as ft
from datetime import datetime
from base.app import App


class DevLog:
    def __init__(self, msg: str, importance: str) -> None:
        self.msg: str = msg
        self.ts: datetime = datetime.now()
        self.importance: str = importance


class DevLogs(ft.Tab):
    _instance: DevLogs | None = None

    def __init__(self, app: App) -> None:
        DevLogs._instance: DevLogs | None = self
        self.logs: list[DevLog] = []
        super().__init__(  # type: ignore
            text="Dev Logs",
            content=ft.Column(controls=[ft.Text("No logs yet. Do stuff")]),
            icon=ft.Icons.CODE,
        )

    @staticmethod
    def log(msg: str, importance: str) -> None:
        self: None | DevLogs = DevLogs._instance
        self.logs.append(DevLog(msg, importance))
        self.content = ft.Column(
            controls=[
                ft.Container(
                    ft.Row(
                        [
                            ft.Text(log.ts.strftime("%d/%m/%Y %H:%M:%S")),
                            ft.Text(
                                log.msg,
                                color=(
                                    ft.Colors.GREY
                                    if log.importance == "info"
                                    else (
                                        ft.Colors.YELLOW
                                        if log.importance == "warning"
                                        else ft.Colors.RED
                                    )
                                ),
                            ),
                        ],
                        tight=True,
                    ),
                    padding=10,
                    border_radius=ft.border_radius.all(8),
                    bgcolor=ft.Colors.GREY_900,
                    margin=ft.Margin(0, 10, 0, 0),
                )
                for log in self.logs
            ],
            scroll=ft.ScrollMode.ALWAYS,
            spacing=10,
        )
        self.update()
