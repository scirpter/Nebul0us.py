import flet as ft

from base.app import App


class AbuseTab(ft.Tab):

    def __init__(self, app: App) -> None:
        super().__init__(
            text="Abuse",
            content=ft.Container(
                alignment=ft.alignment.top_left,
                content=ft.Column(
                    [
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text(
                                        "Sign-in Token",
                                        style=ft.TextStyle(
                                            20,
                                            weight=ft.FontWeight.BOLD,
                                            decoration=ft.TextDecoration.UNDERLINE,
                                        ),
                                    ),
                                    ft.TextField(
                                        label="Token here", border_color=ft.colors.GREY
                                    ),
                                    ft.TextButton(
                                        text="Submit",
                                        icon=ft.icons.CHECK,
                                        icon_color=ft.colors.GREEN,
                                    ),
                                ]
                            ),
                            margin=ft.Margin(0, 10, 0, 80),
                        ),
                        #
                        ft.Column(
                            [
                                ft.TextButton(
                                    icon=ft.icons.DELETE_FOREVER_OUTLINED,
                                    icon_color=ft.colors.RED,
                                    text="Delete Account",
                                ),
                                ft.Row(
                                    [
                                        ft.TextButton(
                                            icon=ft.icons.PERSON_OFF,
                                            icon_color=ft.colors.RED,
                                            text="Ban Account Within 1 Day",
                                        ),
                                        ft.Dropdown(
                                            label="Method",
                                            options=[
                                                ft.dropdown.Option(
                                                    text="Spam Mods With Insultive Mails"
                                                ),
                                                ft.dropdown.Option(
                                                    text="Act Like A Bot In-Game Until Reported"
                                                ),
                                            ],
                                            border_color=ft.colors.GREY,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        #
                        ft.Column(
                            [
                                ft.TextButton(
                                    icon=ft.icons.MONEY_OFF,
                                    icon_color=ft.colors.RED,
                                    text="Waste All Plasma",
                                )
                            ]
                        ),
                        #
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.TextButton(
                                            icon=ft.icons.GROUP_OFF,
                                            icon_color=ft.colors.RED,
                                            text="Destroy Clan",
                                            on_click=lambda x: app.notify(  # type: ignore
                                                "Abuse",
                                                "Action not implemented",
                                            ),
                                        ),
                                        ft.Dropdown(
                                            label="Action",
                                            options=[
                                                ft.dropdown.Option(
                                                    text="Kick All Possible Members"
                                                ),
                                                ft.dropdown.Option(
                                                    text="Ban All Possible Members"
                                                ),
                                                ft.dropdown.Option(text="Change Owner"),
                                                ft.dropdown.Option(text="Delete"),
                                            ],
                                            border_color=ft.colors.GREY,
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
            ),
        )
