import flet as ft
from base.app import App
from game.models.client.client import Client


class BotsTab(ft.Tab):
    def __init__(self, app: App) -> None:
        self.app: App = app
        self.logs: list[BotsTab] = []
        super().__init__(
            text="Bots",
            content=ft.Column(
                [
                    ft.Container(
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.TextButton(
                                            text="Add Bot",
                                            icon_color=ft.colors.GREEN,
                                            icon=ft.icons.ADD,
                                            on_click=self.on_add_bot,
                                        ),
                                        ft.TextButton(
                                            text="Kill All Bots",
                                            icon_color=ft.colors.RED,
                                            icon=ft.icons.CLEAR_ALL,
                                            on_click=self.on_kill_all_bots,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        margin=ft.Margin(0, 2, 0, 0),
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                margin=ft.Margin(0, 2, 0, 0),
                                border=ft.Border(
                                    ft.BorderSide(2, ft.colors.GREY_700),
                                    ft.BorderSide(2, ft.colors.GREY_700),
                                    ft.BorderSide(2, ft.colors.GREY_700),
                                    ft.BorderSide(2, ft.colors.GREY_700),
                                ),
                                border_radius=ft.BorderRadius(10, 10, 10, 10),
                                width=app.page.width - 20,
                                height=app.page.height / 1.4,
                            ),
                            ft.Container(
                                margin=ft.Margin(0, 2, 0, 0),
                                border=ft.Border(
                                    ft.BorderSide(2, ft.colors.GREY_700),
                                    ft.BorderSide(2, ft.colors.GREY_700),
                                    ft.BorderSide(2, ft.colors.GREY_700),
                                    ft.BorderSide(2, ft.colors.GREY_700),
                                ),
                                border_radius=ft.BorderRadius(10, 10, 10, 10),
                                width=app.page.width - 20,
                                height=app.page.height / 1.4,
                            ),
                        ],
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ),
        )

    def on_add_bot(self, e: ft.ControlEvent) -> None:
        bot_name = ft.Ref[ft.TextField]()
        slider_ref = ft.Ref[ft.Slider]()

        def dismiss(e: ft.ControlEvent) -> None:
            dlg_modal.open = False
            e.page.update()

        def confirm(e: ft.ControlEvent) -> None:
            if not bot_name.current.value:
                self.app.notify("Botnet", "Bot name can't be empty")
                return
            dlg_modal.open = False
            e.page.update()

            for i in range(int(slider_ref.current.value)):  # type: ignore
                name: str = f"{bot_name.current.value}{(i) if slider_ref.current.value > 1 else ''}"  # type: ignore
                # check if any existant client has the name
                if any(client.client_data.name == name for client in self.app.clients):
                    self.app.notify(
                        "Failure",
                        f"Bot with name {bot_name.current.value} already exists",
                    )
                    continue
                client = Client(self.app)
                client.client_data.name = name  # type: ignore
                self.app.clients.append(client)
                self.app.notify("Botnet", f"Added {client.client_data.name}")

        def on_slider_edit(e: ft.ControlEvent) -> None:
            slider.label = str(int(e.control.value))
            slider.update()

        slider = ft.Slider(
            value=1,
            min=1,
            max=31,
            on_change=on_slider_edit,
            divisions=30,
            ref=slider_ref,
        )

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Configure your bot"),
            content=ft.Column(
                [
                    ft.Text(
                        "⚠️ Running more than 4 clients will require you to use proxies or VPN. Max 4 clients per IP ⚠️",
                        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                        color=ft.colors.GREY_700,
                    ),
                    ft.TextField(
                        label="Bot Name", border_color=ft.colors.GREY_700, ref=bot_name
                    ),
                    ft.Text(
                        "Select the number of bot instances you want to add",
                        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                    ),
                    slider,
                ]
            ),
            actions=[
                ft.TextButton("Confirm", on_click=confirm),
                ft.TextButton("Cancel", on_click=dismiss),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.colors.BLACK,
        )

        e.page.dialog = dlg_modal
        dlg_modal.open = True
        e.page.update()

    def on_kill_all_bots(self, e: ft.ControlEvent) -> None:
        ct: int = len(self.app.clients)
        for client in self.app.clients:
            client.running = False
        self.app.notify("Botnet", f"Killing {ct} bot(s)...")

    def on_disconnect_all_bots(self, e: ft.ControlEvent) -> None:
        ct: int = len(self.app.clients)
        self.app.notify("Botnet", f"Disconnecting {ct} bot(s)...")
