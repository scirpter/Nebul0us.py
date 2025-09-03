from typing import Any
import flet as ft
from base.app import App
from game.api import CoinPurchase, DeleteAccount


class AbuseTab(ft.Tab):
    def __init__(self, app: App) -> None:
        self.app: App = app
        self.sign_in_token_ref = ft.Ref[ft.TextField]()
        self.send_plasma_target_ref = ft.Ref[ft.TextField]()
        self.send_plasma_amount_ref = ft.Ref[ft.TextField]()

        super().__init__(  # type: ignore
            text="Abuse",
            icon=ft.Icons.WARNING,
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
                                        label="Token here",
                                        border_color=ft.Colors.GREY,
                                        ref=self.sign_in_token_ref,
                                    ),
                                ]
                            ),
                            margin=ft.Margin(0, 10, 0, 80),
                        ),
                        ft.Column(
                            [
                                ft.TextButton(
                                    icon=ft.Icons.DELETE_FOREVER_OUTLINED,
                                    icon_color=ft.Colors.RED,
                                    text="Delete Account",
                                    on_click=self.on_delete_account,
                                ),
                                ft.Row(
                                    [
                                        ft.TextButton(
                                            icon=ft.Icons.PERSON_OFF,
                                            icon_color=ft.Colors.RED,
                                            text="Ban Account Within 1 Day",
                                        ),
                                        ft.Dropdown(
                                            label="Method",
                                            options=[
                                                ft.dropdown.Option(
                                                    text="Xbox 360 Voice Message"
                                                ),
                                                ft.dropdown.Option(
                                                    text="Actor"
                                                ),
                                            ],
                                            border_color=ft.Colors.GREY,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        ft.TextButton(
                            icon=ft.Icons.MONEY_OFF,
                            icon_color=ft.Colors.RED,
                            text="Waste All Plasma",
                        ),
                        ft.Row(
                            [
                                ft.TextButton(
                                    icon=ft.Icons.GROUP_OFF,
                                    icon_color=ft.Colors.RED,
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
                                    border_color=ft.Colors.GREY,
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.TextButton(
                                    icon=ft.Icons.MONEY,
                                    icon_color=ft.Colors.RED,
                                    text="Send Plasma",
                                    on_click=self.on_send_plasma,
                                ),
                                ft.TextField(
                                    label="Target ID",
                                    border_color=ft.Colors.GREY,
                                    ref=self.send_plasma_target_ref,
                                    value="12409385",
                                ),
                                ft.TextField(
                                    label="Price",
                                    border_color=ft.Colors.GREY,
                                    ref=self.send_plasma_amount_ref,
                                    value="100",
                                ),
                            ]
                        ),
                    ]
                ),
            ),
        )

    def on_delete_account(self, e: ft.ControlEvent) -> None:
        token: str | None = self.sign_in_token_ref.current.value
        if not token:
            self.app.notify("Abuse", "Invalid sign-in token")
            return

        response: dict[Any, Any] | Exception = DeleteAccount(token).execute()

        if isinstance(response, Exception):
            self.app.notify("Abuse", f"Failed to delete account: {response}")
            return

        if response.get("Error"):
            self.app.notify(
                "Abuse", f"Failed to delete account: {response['Error']}"
            )
            return

        self.app.notify("Abuse", "Account deleted")

    def on_send_plasma(self, e: ft.ControlEvent) -> None:
        target_id: str | None = self.send_plasma_target_ref.current.value
        if not target_id or not target_id.isdigit():
            self.app.notify("Abuse", "Invalid target account ID")
            return

        amount: str | None = self.send_plasma_amount_ref.current.value
        if not amount or not amount.isdigit():
            self.app.notify("Abuse", "Invalid plasma amount")
            return

        ticket: str | None = self.sign_in_token_ref.current.value
        if not ticket:
            self.app.notify("Abuse", "Invalid sign-in token")
            return

        response: dict[Any, Any] | Exception = CoinPurchase(
            ticket, "GIVE_PLASMA", int(target_id), int(amount)
        ).execute()

        if isinstance(response, Exception):
            self.app.notify("Abuse", f"Failed to send plasma: {response}")
            return

        if response.get("Error"):
            self.app.notify(
                "Abuse", f"Failed to send plasma: {response['Error']}"
            )
            return

        coins_spent: int = response.get("CoinsSpent", 0)
        coins_remaining: int = response.get("CoinsRemaining", 0)
        self.app.notify(
            "API",
            f"Sent {coins_spent} plasma to {target_id}, {coins_remaining} remaining",
        )
