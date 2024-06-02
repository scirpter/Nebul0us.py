import flet as ft
from base.app import App
from helpers.config_integrity import save_config


class GeneralSettingsTab(ft.Tab):
    def __init__(self, app: App) -> None:
        self.app: App = app

        super().__init__(
            text="General Settings",
            content=ft.Container(
                alignment=ft.alignment.top_left,
                margin=ft.Margin(0, 10, 0, 0),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Switch(label="Detect Moderators"),
                                ft.Icon(
                                    ft.icons.QUESTION_MARK_OUTLINED,
                                    tooltip="Can't detect hidden lobby joins",
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Switch(label="Block Kicks"),
                                ft.Icon(
                                    ft.icons.QUESTION_MARK_OUTLINED,
                                    tooltip="Bots will still be kicked, but they'll rejoin instantly",
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Switch(label="Trace Packets"),
                                ft.Icon(
                                    ft.icons.QUESTION_MARK_OUTLINED,
                                    tooltip="Only use this if you know what you're doing. Can cause a big performance hit",
                                ),
                            ],
                        ),
                        ft.Switch(label="Auto-Save Config"),
                        ft.TextButton(
                            "Save Config",
                            icon=ft.icons.SAVE,
                            icon_color=ft.colors.GREEN,
                            on_click=self.on_save_config,
                        ),
                    ]
                ),
            ),
        )

    def on_save_config(self, e: ft.ControlEvent) -> None:
        save_config(self.app.statery)
        self.app.notify("Config", "Saved config")
