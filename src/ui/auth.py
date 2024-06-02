import flet as ft

from base.app import App


def key_info_row(k: str, v: str) -> ft.Row:
    return ft.Row(
        [
            ft.Text(f"{k}: ", color=ft.colors.GREY),
            ft.Text(v, selectable=True),
        ]
    )


class AuthTab(ft.Tab):
    def __init__(self, app: App) -> None:
        self.logs: list[AuthTab] = []
        super().__init__(
            text="Auth",
            content=ft.Column(
                [
                    ft.Container(margin=ft.Margin(0, 10, 0, 0)),
                    ft.Text(
                        "You're not logged in.",
                        color=ft.colors.RED,
                    ),
                    ft.TextField(label="License Key", border_color=ft.colors.GREY),
                    ft.Row(
                        [
                            ft.TextButton(
                                text="Submit",
                                icon=ft.icons.CHECK,
                                icon_color=ft.colors.GREEN,
                            ),
                        ]
                    ),
                    ft.Container(
                        margin=ft.Margin(0, 80, 0, 0),
                    ),
                    ft.Text(
                        "Key Information",
                        style=ft.TextStyle(
                            20,
                            weight=ft.FontWeight.BOLD,
                            decoration=ft.TextDecoration.UNDERLINE,
                        ),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                key_info_row("Key", "Signature"),
                                key_info_row("Expires", "Never"),
                                key_info_row("Status", "Active"),
                                key_info_row("Owner Nick", "The Owner"),
                                key_info_row("Owner Discord ID", "0"),
                                key_info_row("Banned?", "No"),
                                key_info_row("Ban Reason", "N/A"),
                            ]
                        )
                    ),
                ]
            ),
        )
