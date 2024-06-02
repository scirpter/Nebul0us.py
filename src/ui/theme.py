import flet as ft
from base.app import App
from base.constants import VALID_HEX_CHARS


class ThemeTab(ft.Tab):
    def __init__(self, app: App) -> None:
        self.app: App = app
        self.background_image_file_picker = ft.FilePicker(
            on_result=self.pick_files_result
        )
        app.page.overlay.append(self.background_image_file_picker)

        super().__init__(
            text="Theme",
            content=ft.Container(
                alignment=ft.alignment.top_left,
                content=ft.Container(
                    ft.Column(
                        [
                            ft.TextField(
                                label="Background Color Hex",
                                on_change=self.on_background_color_change,
                                border_color=ft.colors.GREY,
                            ),
                            ft.TextField(
                                label="Primary Color Hex",
                                on_change=self.on_primary_text_color_change,
                                border_color=ft.colors.GREY,
                            ),
                            ft.TextField(
                                label="Secondary Color Hex",
                                on_change=self.on_secondary_text_color_change,
                                border_color=ft.colors.GREY,
                            ),
                            ft.TextField(
                                label="Tertiary Color Hex",
                                on_change=self.on_tertiary_text_color_change,
                                border_color=ft.colors.GREY,
                            ),
                            ft.Row(
                                [
                                    ft.TextButton(
                                        "Switch Background",
                                        icon=ft.icons.IMAGE,
                                        on_click=self.on_file_picker_click,
                                    ),
                                    ft.TextButton(
                                        "Reset Background",
                                        icon=ft.icons.CLEAR,
                                        on_click=self.on_reset_background,
                                    ),
                                ]
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Background Image Opacity",
                                        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                    ),
                                    ft.Slider(
                                        value=self.app.statery["theme"][
                                            "background_image_opacity"
                                        ],
                                        label="Background Image Opacity",
                                        min=0,
                                        max=1,
                                        divisions=10,
                                        on_change=self.on_background_image_opacity_change,
                                    ),
                                ],
                                spacing=0,
                            ),
                        ]
                    ),
                    margin=ft.Margin(0, 10, 0, 0),
                ),
            ),
        )

    def on_background_image_opacity_change(self, e: ft.ControlEvent) -> None:
        self.app.statery["theme"]["background_image_opacity"] = e.control.value
        self.app.statery["background_image_container"].image_opacity = e.control.value
        self.app.statery["background_image_container"].update()

    def pick_files_result(self, e: ft.FilePickerResultEvent) -> None:
        if not e.files:
            return

        self.app.statery["theme"]["background_image_url"] = e.files[0].path
        self.app.statery["background_image_container"].image_src = self.app.statery[
            "theme"
        ]["background_image_url"]
        self.app.statery["background_image_container"].update()

    def on_reset_background(self, e: ft.ControlEvent) -> None:
        self.app.statery["theme"]["background_image_url"] = ""
        self.app.statery["background_image_container"].image_src = ""
        self.app.statery["background_image_container"].update()

    def on_file_picker_click(self, e: ft.ControlEvent) -> None:
        self.background_image_file_picker.pick_files(
            "Select a background image",
            file_type=ft.FilePickerFileType.IMAGE,
            allowed_extensions=["png", "jpg", "jpeg"],
        )

    def update_theme(self, hexz: str) -> None:
        self.app.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=self.app.statery["theme"]["primary_color_hex"],
                secondary=self.app.statery["theme"]["secondary_color_hex"],
                tertiary=self.app.statery["theme"]["tertiary_color_hex"],
            )
        )
        self.app.page.update()
        self.app.notify("Theme", f"Set color to #{hexz}")

    def on_background_color_change(self, e: ft.ControlEvent) -> None:
        if len(e.control.value) != 6 or not all(
            c.lower() in VALID_HEX_CHARS for c in e.control.value  # type: ignore
        ):
            return
        self.app.statery["theme"]["background_color_hex"] = "#" + e.control.value
        self.page.bgcolor = f"#{e.control.value}"
        self.update_theme(e.control.value)

    def on_primary_text_color_change(self, e: ft.ControlEvent) -> None:
        if len(e.control.value) != 6 or not all(
            c.lower() in VALID_HEX_CHARS for c in e.control.value  # type: ignore
        ):
            return
        self.app.statery["theme"]["primary_color_hex"] = "#" + e.control.value
        self.update_theme(e.control.value)

    def on_secondary_text_color_change(self, e: ft.ControlEvent) -> None:
        if len(e.control.value) != 6 or not all(
            c.lower() in VALID_HEX_CHARS for c in e.control.value  # type: ignore
        ):
            return
        self.app.statery["theme"]["secondary_color_hex"] = "#" + e.control.value
        self.update_theme(e.control.value)

    def on_tertiary_text_color_change(self, e: ft.ControlEvent) -> None:
        if len(e.control.value) != 6 or not all(
            c.lower() in VALID_HEX_CHARS for c in e.control.value  # type: ignore
        ):
            return
        self.app.statery["theme"]["tertiary_color_hex"] = "#" + e.control.value
        self.update_theme(e.control.value)
