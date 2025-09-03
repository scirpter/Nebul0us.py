from threading import Thread
from time import sleep
import flet as ft
from base.app import App
from helpers.config_integrity import save_config


class GeneralSettingsTab(ft.Tab):
    def __init__(self, app: App) -> None:
        self.app: App = app
        self.auto_save_toggle = ft.Ref[ft.Switch]()
        self.trace_packets_toggle = ft.Ref[ft.Switch]()
        self.detect_moderators_toggle = ft.Ref[ft.Switch]()
        Thread(target=self.save_config_loop).start()

        super().__init__(  # type: ignore
            text="General Settings",
            icon=ft.Icons.SETTINGS,
            content=ft.Container(
                alignment=ft.alignment.top_left,
                margin=ft.Margin(0, 10, 0, 0),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Switch(
                                    label="Detect Moderators",
                                    ref=self.detect_moderators_toggle,
                                    on_change=self.on_detect_moderators,
                                ),
                                ft.Icon(
                                    ft.Icons.QUESTION_MARK_OUTLINED,
                                    tooltip="Can't detect hidden lobby joins",
                                ),
                            ]
                        ),
                        ft.Switch(
                            label="Auto-Save Config",
                            ref=self.auto_save_toggle,
                            value=self.app.states["general_settings"][
                                "auto_save_config"
                            ],
                        ),
                        ft.TextButton(
                            "Save Config",
                            icon=ft.Icons.SAVE,
                            on_click=self.on_save_config,
                        ),
                    ]
                ),
            ),
        )

    def on_detect_moderators(self, e: ft.ControlEvent) -> None:
        self.app.states["general_settings"][
            "detect_moderators"
        ] = self.detect_moderators_toggle.current.value  # type: ignore

    def on_trace_packets(self, e: ft.ControlEvent) -> None:
        self.app.states["general_settings"][
            "trace_packets"
        ] = self.trace_packets_toggle.current.value  # type: ignore

    def save_config_loop(self) -> None:
        previous = str(self.app.states)
        while 1:
            if not self.auto_save_toggle.current:
                sleep(0.1)
                continue
            if not self.auto_save_toggle.current.value:
                if self.app.states["general_settings"]["auto_save_config"]:
                    self.app.states["general_settings"]["auto_save_config"] = False
                sleep(0.1)
                continue
            else:
                if not self.app.states["general_settings"]["auto_save_config"]:
                    self.app.states["general_settings"]["auto_save_config"] = True

            if previous != str(self.app.states):
                previous = str(self.app.states)
                save_config(self.app.states)

            sleep(0.1)

    def on_save_config(self, e: ft.ControlEvent) -> None:
        if self.app.states["general_settings"]["auto_save_config"]:
            self.app.notify("Config", "No need to save. Auto-save is enabled")
            return
        save_config(self.app.states)
        self.app.notify("Config", "Saved config")
