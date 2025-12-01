from __future__ import annotations

from typing import Any

from nicegui import ui

from base.app import App
from game.api import CoinPurchase, DeleteAccount
from ui.components.cards import glass_card


def render(app: App) -> None:
    with glass_card():
        ui.label("Account Actions").classes("text-lg font-semibold text-slate-100")
        ui.label("Dangerous API calls for moderation testing. Use responsibly.").classes("text-sm text-amber-300")
        token_input = ui.input(label="Sign-in Token", placeholder="Paste token").props("type=password").classes(
            "w-full md:w-[420px]"
        )

        ui.button(
            "Delete Account",
            icon="delete_forever",
            on_click=lambda: _delete_account(app, token_input.value or ""),
        ).classes("bg-rose-500/80 text-slate-100 w-fit")

    with glass_card():
        ui.label("Clan Tools").classes("text-lg font-semibold text-slate-100")
        ui.label("Placeholder actions for clan administration.").classes("text-sm text-slate-400")
        ui.button(
            "Destroy Clan",
            icon="group_off",
            on_click=lambda: app.notify("Abuse", "Action not implemented"),
        ).classes("bg-slate-800 text-slate-200 w-fit")

    with glass_card():
        ui.label("Plasma Transfer").classes("text-lg font-semibold text-slate-100")
        ui.label(
            "Send plasma to another account. Requires a valid sign-in token with sufficient balance."
        ).classes("text-sm text-slate-400")
        with ui.row().classes("gap-4 flex-wrap"):
            plasma_target = ui.input(label="Target Account ID", value="12409385").classes("w-full md:w-64")
            plasma_amount = ui.input(label="Plasma Amount", value="100").classes("w-full md:w-64")
        ui.button(
            "Send Plasma",
            icon="paid",
            on_click=lambda: _send_plasma(
                app,
                token_input.value or "",
                plasma_target.value or "",
                plasma_amount.value or "",
            ),
        ).classes("bg-emerald-500/80 hover:bg-emerald-400 text-slate-900 w-fit")


def _delete_account(app: App, token: str) -> None:
    if not token:
        app.notify("Abuse", "Invalid sign-in token")
        return
    response: dict[str, Any] | Exception = DeleteAccount(token).execute()
    if isinstance(response, Exception):
        app.notify("Abuse", f"Failed to delete account: {response}")
        return
    if response.get("Error"):
        app.notify("Abuse", f"Failed to delete account: {response['Error']}")
        return
    app.notify("Abuse", "Account deleted")


def _send_plasma(app: App, token: str, target: str, amount: str) -> None:
    if not token:
        app.notify("Abuse", "Invalid sign-in token")
        return
    if not target or not target.isdigit():
        app.notify("Abuse", "Invalid target account ID")
        return
    if not amount or not amount.isdigit():
        app.notify("Abuse", "Invalid plasma amount")
        return

    response: dict[str, Any] | Exception = CoinPurchase(
        token, "GIVE_PLASMA", int(target), int(amount)
    ).execute()

    if isinstance(response, Exception):
        app.notify("Abuse", f"Failed to send plasma: {response}")
        return
    if response.get("Error"):
        app.notify("Abuse", f"Failed to send plasma: {response['Error']}")
        return

    spent = response.get("CoinsSpent", 0)
    remaining = response.get("CoinsRemaining", 0)
    app.notify("API", f"Sent {spent} plasma to {target}. {remaining} remaining.")
