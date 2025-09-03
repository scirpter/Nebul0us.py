from __future__ import annotations
import flet as ft

from base.app import App


class BinTab(ft.Tab):
    def __init__(self, app: App) -> None:
        super().__init__(  # type: ignore
            text="Bin",
            icon=ft.Icons.DELETE,
            content=ft.Column(
                controls=[
                    ft.Container(margin=ft.Margin(0, 10, 0, 0)),
                    ft.TextField(
                        app.states["bin_text"],
                        border_color=ft.Colors.GREY,
                        shift_enter=True,
                        on_change=self.on_bin_text_change,
                    ),
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ),
        )
        self.app: App = app

    def on_bin_text_change(self, e: ft.ControlEvent) -> None:
        self.app.states["bin_text"] = e.control.value  # type: ignore
