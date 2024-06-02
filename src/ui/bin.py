from __future__ import annotations
import flet as ft

from base.app import App


class BinTab(ft.Tab):
    def __init__(self, app: App) -> None:
        super().__init__(
            text="Bin",
            content=ft.Column(
                controls=[
                    ft.Container(margin=ft.Margin(0, 10, 0, 0)),
                    ft.TextField(
                        app.statery["bin_text"],
                        border_color=ft.colors.GREY,
                        shift_enter=True,
                        on_change=self.on_bin_text_change,
                    ),
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ),
        )
        self.app: App = app

    def on_bin_text_change(self, e: ft.ControlEvent) -> None:
        self.app.statery["bin_text"] = e.control.value
