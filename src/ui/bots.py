import flet as ft
from base.app import App
from game.enums.game_mode import GAME_MODE
from game.models.client.client import Client
from game.enums import REGION


class BotsTab(ft.Tab):
    def __init__(self, app: App) -> None:
        self.app: App = app
        self.logs: list[BotsTab] = []
        super().__init__(  # type: ignore
            text="Bots", content=self.generate_content(), icon=ft.Icons.ANDROID
        )

    def generate_content(self) -> ft.Column:
        return ft.Column(
            [
                ft.Container(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.TextButton(
                                        text="Add Bot",
                                        icon_color=ft.Colors.GREEN,
                                        icon=ft.Icons.ADD,
                                        on_click=self.on_add_bot,
                                    ),
                                    ft.TextButton(
                                        text="Disconnect all bots",
                                        icon_color=ft.Colors.RED,
                                        icon=ft.Icons.CLEAR_ALL,
                                        on_click=self.on_kill_all_bots,
                                    ),
                                ]
                            ),
                        ]
                    ),
                    margin=ft.Margin(0, 2, 0, 0),
                ),
                *self.generate_bot_rows(),
            ],
            scroll=ft.ScrollMode.ALWAYS,
        )

    def generate_bot_rows(self) -> list[ft.Row]:
        rows: list[ft.Row] = []
        for client in self.app.clients:
            new_bot_name_ref = ft.Ref[ft.TextField]()
            active_keep_alive_ms_text = ft.Ref[ft.Text]()
            idle_keep_alive_ms_text = ft.Ref[ft.Text]()

            region_selection = ft.Ref[ft.Dropdown]()
            gamemode_selection = ft.Ref[ft.Dropdown]()
            is_mayhem_checkbox = ft.Ref[ft.Switch]()
            is_connect_in_private_search_checkbox = ft.Ref[ft.Switch]()

            def validate_bot_name(
                e: ft.ControlEvent, client: Client = client
            ) -> None:
                name: str = new_bot_name_ref.current.value  # type: ignore
                if name == client.client_data.name:
                    self.app.notify("Session", "No changes made. :?")
                    return
                elif any(
                    client.client_data.name == name
                    for client in self.app.clients
                ):
                    self.app.notify(
                        "Session", "Bot with this name already exists"
                    )
                    return
                elif not name:
                    self.app.notify("Session", "Bot name can't be empty")
                    return
                elif len(name) > 12:
                    self.app.notify(
                        "Session", "Bot name can't be longer than 12 characters"
                    )
                    return
                client.client_data.name = name
                client.settings["player_name"] = name
                self.update()
                self.app.notify("Session", f"Set bot name to {name}")

            def on_goto_closest_holes_checkbox(
                e: ft.ControlEvent, client: Client = client
            ) -> None:
                client.options_data.chase_nearest_holes = e.control.value  # type: ignore

            def on_auto_respawn_checkbox(
                e: ft.ControlEvent, client: Client = client
            ) -> None:
                client.options_data.auto_respawn = e.control.value  # type: ignore

            def on_keep_alive_active_slider(
                e: ft.ControlEvent, client: Client = client
            ) -> None:
                client.settings["active_keep_alive_ms"] = int(e.control.value)  # type: ignore
                active_keep_alive_ms_text.current.value = f"Active Keep Alive ({client.settings['active_keep_alive_ms']} MS)"
                self.update()

            def on_keep_alive_idle_slider(
                e: ft.ControlEvent, client: Client = client
            ) -> None:
                client.settings["idle_keep_alive_ms"] = int(e.control.value)  # type: ignore
                idle_keep_alive_ms_text.current.value = f"Idle Keep Alive ({client.settings['idle_keep_alive_ms']} MS)"
                self.update()

            def connect(e: ft.ControlEvent, client: Client = client) -> None:
                if client.is_connected:
                    self.app.notify("Session", "Bot is already connected. :|")
                    return
                if not region_selection.current.value:
                    self.app.notify(
                        "Session", "Please select a proper region. :?"
                    )
                    return

                r = client.connect(
                    region=region_selection.current.value,
                    mayhem=is_mayhem_checkbox.current.value,  # type: ignore
                    connect_in_private_search=is_connect_in_private_search_checkbox.current.value,  # type: ignore
                    game_mode=GAME_MODE.from_string(
                        gamemode_selection.current.value
                        or GAME_MODE.FFA_ULTRA.name
                    ),  # type: ignore
                )
                if isinstance(r, Exception):
                    self.app.notify(
                        "Connection Error", f"Failed to connect: {r}"
                    )
                    return

            def start_playing(
                e: ft.ControlEvent, client: Client = client
            ) -> None:
                if not client.is_connected:
                    self.app.notify(
                        "Session",
                        f"{client.client_data.name} is not connected. :|",
                    )
                    return
                client.start_playing()
                self.app.notify(
                    "Player", f"{client.client_data.name} sent play request"
                )

            def disconnect(e: ft.ControlEvent, client: Client = client) -> None:
                if not client.is_connected:
                    self.app.notify("Session", "Bot is not connected. :|")
                    return
                client.disconnect()
                self.app.notify(
                    "Lobby",
                    f"{client.client_data.name} disconnected from the surface",
                )

            def copy_token(e: ft.ControlEvent, client: Client = client) -> None:
                self.app.page.set_clipboard(client.client_data.login_ticket)
                self.app.notify("Info", "Copied bot token to clipboard")

            rows.append(
                ft.Row(
                    [
                        ft.Container(
                            padding=ft.padding.all(9),
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Dropdown(
                                                label="Region",
                                                options=[
                                                    ft.dropdown.Option(
                                                        text=region
                                                    )
                                                    for region in REGION.all()
                                                ],
                                                border_color=ft.Colors.GREY,
                                                ref=region_selection,
                                                value=REGION.EU.name,
                                            ),
                                            ft.Dropdown(
                                                label="Game Mode",
                                                options=[
                                                    ft.dropdown.Option(
                                                        text=mode
                                                    )
                                                    for mode in GAME_MODE.all()
                                                ],
                                                border_color=ft.Colors.GREY,
                                                ref=gamemode_selection,
                                                value=GAME_MODE.FFA_ULTRA.name,
                                            ),
                                            ft.Checkbox(
                                                label="Mayhem",
                                                ref=is_mayhem_checkbox,
                                                value=False,
                                            ),
                                            ft.Checkbox(
                                                label="Connect in private game search",
                                                ref=is_connect_in_private_search_checkbox,
                                                value=False,
                                            ),
                                            ft.Checkbox(
                                                label="Autorespawn",
                                                value=True,
                                                on_change=on_auto_respawn_checkbox,
                                            ),
                                            ft.Checkbox(
                                                label="Goto Closest Holes",
                                                value=False,
                                                on_change=on_goto_closest_holes_checkbox,
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.TextField(
                                                value=client.client_data.name,
                                                text_style=ft.TextStyle(
                                                    weight=ft.FontWeight.BOLD
                                                ),
                                                ref=new_bot_name_ref,
                                                label="Bot Name",
                                            ),
                                            ft.TextButton(
                                                "Validate & Apply",
                                                on_click=validate_bot_name,
                                            ),
                                            ft.TextButton(
                                                "Delete Bot",
                                                on_click=self.delete_bot,
                                                key=str(client.client_data.uid),
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        [
                                            ft.Column(
                                                [
                                                    ft.Row(
                                                        [
                                                            ft.Text(
                                                                f"Active Keep Alive ({client.settings['active_keep_alive_ms']} MS)",
                                                                weight=ft.FontWeight.BOLD,
                                                                ref=active_keep_alive_ms_text,
                                                            ),
                                                            ft.Icon(
                                                                ft.Icons.QUESTION_MARK_OUTLINED,
                                                                tooltip="Recommended: 52MS",
                                                            ),
                                                        ]
                                                    ),
                                                    ft.Slider(
                                                        max=600,
                                                        value=client.settings[
                                                            "active_keep_alive_ms"
                                                        ],
                                                        on_change=on_keep_alive_active_slider,
                                                    ),
                                                ]
                                            ),
                                            ft.Column(
                                                [
                                                    ft.Row(
                                                        [
                                                            ft.Text(
                                                                f"Idle Keep Alive ({client.settings['idle_keep_alive_ms']} MS)",
                                                                weight=ft.FontWeight.BOLD,
                                                                ref=idle_keep_alive_ms_text,
                                                            ),
                                                            ft.Icon(
                                                                ft.Icons.QUESTION_MARK_OUTLINED,
                                                                tooltip="Recommended: 502MS",
                                                            ),
                                                        ]
                                                    ),
                                                    ft.Slider(
                                                        max=600,
                                                        value=client.settings[
                                                            "idle_keep_alive_ms"
                                                        ],
                                                        on_change=on_keep_alive_idle_slider,
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.TextButton(
                                                "Start Playing",
                                                icon=ft.Icons.PLAY_ARROW,
                                                icon_color=ft.Colors.GREEN,
                                                on_click=start_playing,
                                            ),
                                            ft.TextButton(
                                                "Connect",
                                                icon=ft.Icons.WIFI,
                                                icon_color=ft.Colors.AMBER,
                                                on_click=connect,
                                            ),
                                            ft.TextButton(
                                                "Disconnect",
                                                icon=ft.Icons.DANGEROUS,
                                                on_click=disconnect,
                                            ),
                                            ft.TextButton(
                                                "Copy Token",
                                                icon=ft.Icons.COPY,
                                                on_click=copy_token,
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            margin=ft.Margin(0, 2, 0, 0),
                            border=ft.Border(
                                ft.BorderSide(2, ft.Colors.GREY_700),
                                ft.BorderSide(2, ft.Colors.GREY_700),
                                ft.BorderSide(2, ft.Colors.GREY_700),
                                ft.BorderSide(2, ft.Colors.GREY_700),
                            ),
                            border_radius=ft.BorderRadius(10, 10, 10, 10),
                            width=(self.app.page.width or 20) - 20,
                            height=(self.app.page.height or 1.4) / 1.4,
                            alignment=ft.alignment.top_left,
                        )
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )

        return rows

    def delete_bot(self, e: ft.ControlEvent) -> None:
        uid: int = int(e.control.key)  # type: ignore
        client: Client | None = next(
            (
                client
                for client in self.app.clients
                if client.client_data.uid == uid
            ),
            None,
        )
        if client is None:
            self.app.notify("Session", f"Account with ID {uid} not found")
            self.content = self.generate_content()
            self.update()
            return

        self.app.clients.remove(client)
        for setting in self.app.states["client_settings"]:
            if setting["client_uid"] == uid:
                self.app.states["client_settings"].remove(setting)
                break
        self.content = self.generate_content()
        self.update()
        self.app.notify("Session", f"Deleted {client.client_data.name}")

    def on_add_bot(self, e: ft.ControlEvent) -> None:
        bot_name = ft.Ref[ft.TextField]()
        bot_ticket = ft.Ref[ft.TextField]()

        def fetch_local_token(e: ft.ControlEvent) -> None:
            bot_ticket.current.value = "THIS FEATURE IS NOT AVAILABLE YET."
            bot_ticket.current.update()

        def dismiss(e: ft.ControlEvent) -> None:
            dlg_modal.open = False
            self.app.page.update()  # type: ignore

        def confirm(e: ft.ControlEvent) -> None:
            if not bot_name.current.value:
                self.app.notify("Session", "Bot name can't be empty")
                return
            elif not bot_ticket.current.value:
                self.app.notify("Session", "Bot ticket can't be empty")
                return
            name: str = bot_name.current.value
            if any(
                client.client_data.name == name for client in self.app.clients
            ):
                self.app.notify(
                    "Failure",
                    f"Bot with name {bot_name.current.value} already exists",
                )
                return
            elif any(
                client.client_data.login_ticket == bot_ticket.current.value
                for client in self.app.clients
            ):
                self.app.notify(
                    "Failure",
                    "Bot with this ticket already exists",
                )
                return

            if (
                not bot_ticket.current.value.endswith("=")
                or "," not in bot_ticket.current.value
            ):
                self.app.notify(
                    "Failure",
                    "Invalid ticket format",
                )
                return

            account_id: str = bot_ticket.current.value.split(",")[0]
            if not account_id.isdigit():
                self.app.notify(
                    "Failure",
                    "Invalid ticket format",
                )
                return

            dlg_modal.open = False
            self.app.page.update()  # type: ignore

            client = Client(
                self.app, int(account_id), name, bot_ticket.current.value
            )
            self.app.clients.append(client)
            self.content = self.generate_content()
            self.update()
            self.app.notify("Session", f"Added {client.client_data.name}")

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Configure your bot"),
            content=ft.Column(
                [
                    ft.Text(
                        "⚠️ Running more than 4 clients will require you to use proxies or VPN. Max 4 clients per IP ⚠️",
                        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                        color=ft.Colors.GREY_700,
                    ),
                    ft.TextField(
                        label="Bot Name",
                        border_color=ft.Colors.GREY_700,
                        ref=bot_name,
                    ),
                    ft.Row(
                        [
                            ft.TextField(
                                label="Bot Ticket",
                                border_color=ft.Colors.GREY_700,
                                ref=bot_ticket,
                            ),
                            ft.TextButton(
                                text="Fetch From Game Files (root)",
                                icon=ft.Icons.REFRESH,
                                icon_color=ft.Colors.AMBER,
                                on_click=fetch_local_token,
                            ),
                        ]
                    ),
                ]
            ),
            actions=[
                ft.TextButton("Confirm", on_click=confirm),
                ft.TextButton("Cancel", on_click=dismiss),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.BLACK,
        )

        self.page.open(dlg_modal)

    def on_kill_all_bots(self, e: ft.ControlEvent) -> None:
        ct: int = len(self.app.clients)
        self.app.notify("Session", f"Killing {ct} bot(s)...")
        for client in self.app.clients:
            client.disconnect()
            self.app.notify("Session", f"Killed {client.client_data.name}")

    def on_disconnect_all_bots(self, e: ft.ControlEvent) -> None:
        ct: int = len(self.app.clients)
        self.app.notify("Session", f"Disconnecting {ct} bot(s)...")
