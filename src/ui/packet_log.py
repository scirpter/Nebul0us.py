from __future__ import annotations
import flet as ft
from datetime import datetime
from base.app import App
from game.models.client.client import Client
from game.packets.packet import Packet


class PacketLog:
    def __init__(self, msg: str, client: Client, packet: Packet) -> None:
        self.msg: str = msg
        self.client: Client = client
        self.packet: Packet = packet
        self.ts: datetime = datetime.now()


class PacketLogsTab(ft.Tab):
    _instance: PacketLogsTab | None = None

    def __init__(self, app: App) -> None:
        PacketLogsTab._instance: PacketLogsTab | None = self
        self.logs: list[PacketLog] = []
        super().__init__(
            text="Packet Logs",
            content=ft.Column(
                controls=[
                    ft.Row(
                        [
                            ft.Text("No logs yet. Do stuff or enable packet tracing"),
                        ]
                    )
                ],
            ),
        )

    @staticmethod
    def log(msg: str, client: Client, packet: Packet) -> None:
        self: None | PacketLogsTab = PacketLogsTab._instance
        self.logs.append(PacketLog(msg, client, packet))
        self.content = ft.Container(
            ft.Column(
                [
                    ft.Dropdown(
                        options=[ft.dropdown.Option("All Bots")], label="Target Bot"
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(
                                [
                                    ft.Text(
                                        log.ts.strftime("%H:%M:%S"),
                                        color=ft.colors.GREY,
                                    ),
                                    ft.Text(
                                        log.packet.__class__.__name__,
                                        color=ft.colors.GREY_400,
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            log.client.client_data.name,
                                            color=ft.colors.PURPLE,
                                            style=ft.TextStyle(
                                                weight=ft.FontWeight.BOLD
                                            ),
                                        ),
                                        border=ft.Border(
                                            ft.BorderSide(2, ft.colors.PURPLE),
                                            ft.BorderSide(2, ft.colors.PURPLE),
                                            ft.BorderSide(2, ft.colors.PURPLE),
                                            ft.BorderSide(2, ft.colors.PURPLE),
                                        ),
                                        border_radius=ft.BorderRadius(5, 5, 5, 5),
                                        padding=ft.Padding(2, 0, 2, 0),
                                    ),
                                    ft.Text(log.msg, color=ft.colors.GREY),
                                ]
                            )
                            for log in reversed(self.logs)
                        ],
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                ]
            ),
            margin=ft.Margin(0, 20, 0, 0),
        )
        self.update()
