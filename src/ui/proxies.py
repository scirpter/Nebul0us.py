from __future__ import annotations
import flet as ft

from base.app import App


class ProxiesTab(ft.Tab):
    _instance: ProxiesTab | None = None

    def __init__(self, app: App) -> None:
        ProxiesTab._instance: ProxiesTab | None = self
        super().__init__(
            text="Proxies",
            content=ft.Column(),
        )
