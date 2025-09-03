from __future__ import annotations
import threading
import time
from typing import Callable
import flet as ft

from base.app import App
from game.models.client.client import Client


class LobbiesTab(ft.Tab):
    def __init__(self, app: App) -> None:
        self.app: App = app

        # Refs
        self.player_id_ref = ft.Ref[ft.TextField]()
        self.lobby_name_ref = ft.Ref[ft.TextField]()
        self.join_btn_ref = ft.Ref[ft.TextButton]()
        self.spectate_btn_ref = ft.Ref[ft.TextButton]()
        self.client_dd_ref = ft.Ref[ft.Dropdown]()
        self.ps_page_text_ref = ft.Ref[ft.Text]()
        self.ps_list_col_ref = ft.Ref[ft.Column]()

        content = ft.Column(
            [
                ft.Container(margin=ft.Margin(0, 10, 0, 0)),
                ft.Text(
                    "Join a lobby by Player ID or Lobby name (fill exactly one)",
                    color=ft.Colors.GREY,
                ),
                ft.Row(
                    [
                        ft.Dropdown(
                            label="Target client",
                            ref=self.client_dd_ref,
                            options=self._build_client_options(),
                            value="ALL",
                            width=320,
                        )
                    ],
                    wrap=True,
                ),
                ft.Row(
                    [
                        ft.TextField(
                            label="Player ID",
                            ref=self.player_id_ref,
                            border_color=ft.Colors.GREY,
                            on_change=self._on_input_change,
                            hint_text="e.g. 123456",
                        ),
                        ft.TextField(
                            label="Lobby name",
                            ref=self.lobby_name_ref,
                            border_color=ft.Colors.GREY,
                            on_change=self._on_input_change,
                            hint_text="e.g. My Lobby",
                        ),
                    ],
                    wrap=True,
                    spacing=12,
                ),
                ft.Row(
                    [
                        ft.TextButton(
                            text="Join",
                            icon=ft.Icons.LOGIN,
                            icon_color=ft.Colors.AMBER,
                            ref=self.join_btn_ref,
                            disabled=True,
                            on_click=self._on_join,
                        ),
                        ft.TextButton(
                            text="Spectate",
                            icon=ft.Icons.VISIBILITY,
                            icon_color=ft.Colors.AMBER,
                            ref=self.spectate_btn_ref,
                            disabled=True,
                            on_click=self._on_spectate,
                        ),
                        ft.TextButton(
                            text="Clear",
                            icon=ft.Icons.CLEAR,
                            on_click=self._on_clear,
                        ),
                    ]
                ),
                ft.Divider(color=ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
                ft.Text(
                    "Private Games",
                    style=ft.TextStyle(
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        decoration=ft.TextDecoration.UNDERLINE,
                    ),
                ),
                ft.Row(
                    [
                        ft.Text("Page:", color=ft.Colors.GREY),
                        ft.Text("-", ref=self.ps_page_text_ref),
                        ft.TextButton(
                            text="Prev",
                            icon=ft.Icons.CHEVRON_LEFT,
                            on_click=self._on_ps_prev,
                        ),
                        ft.TextButton(
                            text="Next",
                            icon=ft.Icons.CHEVRON_RIGHT,
                            on_click=self._on_ps_next,
                        ),
                        ft.TextButton(
                            text="Refresh",
                            icon=ft.Icons.REFRESH,
                            on_click=self._on_ps_refresh,
                        ),
                    ],
                    wrap=True,
                    spacing=10,
                ),
                ft.Container(
                    content=ft.Column(
                        ref=self.ps_list_col_ref,
                        spacing=6,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                    border_radius=ft.BorderRadius(8, 8, 8, 8),
                    padding=10,
                    height=360,
                ),
            ]
        )

        super().__init__(text="Lobbies", icon=ft.Icons.GROUP, content=content)  # type: ignore
        # Lightweight UI refresh timer; networking loop lives in Client
        self._ps_running = True
        self._ps_thread = threading.Thread(
            target=self._ps_ui_refresh_loop, daemon=True
        )
        self._ps_thread.start()
        # Defer the first render a tick to ensure controls are mounted
        threading.Timer(0.05, self._refresh_private_games).start()

    # Validation helpers
    def _validate(self) -> bool:
        pid = (
            (self.player_id_ref.current.value or "").strip()
            if self.player_id_ref.current
            else ""
        )
        name = (
            (self.lobby_name_ref.current.value or "").strip()
            if self.lobby_name_ref.current
            else ""
        )

        both = bool(pid) and bool(name)
        none = (not pid) and (not name)
        ok = not both and not none

        pid_numeric_ok = True
        if pid and not pid.isdigit():
            pid_numeric_ok = False

        if self.player_id_ref.current:
            self.player_id_ref.current.error_text = None
        if self.lobby_name_ref.current:
            self.lobby_name_ref.current.error_text = None

        if both:
            err = "Fill either Player ID or Lobby name, not both"
            if self.player_id_ref.current:
                self.player_id_ref.current.error_text = err
            if self.lobby_name_ref.current:
                self.lobby_name_ref.current.error_text = err
        elif ok and pid and not pid_numeric_ok:
            if self.player_id_ref.current:
                self.player_id_ref.current.error_text = (
                    "Player ID must be numeric"
                )
            ok = False

        if self.join_btn_ref.current:
            self.join_btn_ref.current.disabled = not ok
            self.join_btn_ref.current.update()
        if self.spectate_btn_ref.current:
            self.spectate_btn_ref.current.disabled = not ok
            self.spectate_btn_ref.current.update()

        if self.player_id_ref.current:
            self.player_id_ref.current.update()
        if self.lobby_name_ref.current:
            self.lobby_name_ref.current.update()

        return ok

    def _on_input_change(self, _: ft.ControlEvent) -> None:
        self._validate()

    # Client helpers
    def _build_client_options(self) -> list[ft.dropdown.Option]:
        opts: list[ft.dropdown.Option] = [
            ft.dropdown.Option("ALL", "All clients")
        ]
        for c in self.app.clients:
            opts.append(
                ft.dropdown.Option(
                    str(c.client_data.uid),
                    f"{c.client_data.name} ({c.client_data.uid})",
                )
            )
        return opts

    def _selected_clients(self) -> list[Client]:
        dd = self.client_dd_ref.current
        if not dd or not dd.value or dd.value == "ALL":
            return list(self.app.clients)
        try:
            uid = int(dd.value)
        except ValueError:
            return []
        for c in self.app.clients:
            if c.client_data.uid == uid:
                return [c]
        return []

    # Private Search helpers
    def _get_ps_client(self) -> Client | None:
        for c in self.app.clients:
            if c.private_search_list.entries:
                return c
        return None

    def _ps_set_page(self, delta: int) -> None:
        client = self._get_ps_client()
        if not client:
            return
        client.private_search_list.page = max(
            0, client.private_search_list.page + delta
        )
        client.request_private_search_list()
        self._refresh_private_games()

    def _on_ps_prev(self, _: ft.ControlEvent) -> None:
        self._ps_set_page(-1)

    def _on_ps_next(self, _: ft.ControlEvent) -> None:
        self._ps_set_page(1)

    def _on_ps_refresh(self, _: ft.ControlEvent) -> None:
        client = self._get_ps_client()
        if client:
            client.request_private_search_list()
        self._refresh_private_games()

    def _refresh_private_games(self) -> None:
        col = self.ps_list_col_ref.current
        page_txt = self.ps_page_text_ref.current
        if not col or not page_txt:
            return

        client = self._get_ps_client()
        any_data = any(c.private_search_list.entries for c in self.app.clients)
        if not any_data:
            page_txt.value = "-"
            col.controls = [
                ft.Text(
                    "Connect to private search list first.",
                    color=ft.Colors.GREY,
                )
            ]
            if col.page:
                col.update()
            if page_txt.page:
                page_txt.update()
            return

        if not client:
            client = self.app.clients[0] if self.app.clients else None
            if not client:
                page_txt.value = "-"
                col.controls = [ft.Text("No clients.")]
                if col.page:
                    col.update()
                if page_txt.page:
                    page_txt.update()
                return

        page_txt.value = str(client.private_search_list.page)

        rows: list[ft.Control] = []
        for entry in client.private_search_list.entries:

            def make_copy(name: str) -> Callable[[ft.ControlEvent], None]:
                def _copy(_: ft.ControlEvent) -> None:
                    try:
                        self.app.page.set_clipboard(name)
                        self.app.notify(
                            "Private Games", f"Copied lobby name: {name}"
                        )
                    except Exception:
                        pass

                return _copy

            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(entry.name, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"Players: {entry.players_in_lobby}/{entry.max_players}",
                                color=ft.Colors.GREY,
                            ),
                            ft.Text(
                                f"Mode: {entry.game_mode.name if hasattr(entry.game_mode, 'name') else entry.game_mode}",
                                color=ft.Colors.GREY,
                            ),
                            ft.TextButton(
                                text="Copy Name",
                                icon=ft.Icons.COPY,
                                on_click=make_copy(entry.name),
                            ),
                        ],
                        wrap=True,
                        spacing=14,
                    ),
                    padding=8,
                    border=ft.Border(
                        ft.BorderSide(
                            1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)
                        ),
                        ft.BorderSide(
                            1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)
                        ),
                        ft.BorderSide(
                            1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)
                        ),
                        ft.BorderSide(
                            1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)
                        ),
                    ),
                    border_radius=ft.BorderRadius(6, 6, 6, 6),
                )
            )

        col.controls = rows or [
            ft.Text("No lobbies on this page.", color=ft.Colors.GREY)
        ]
        if col.page:
            col.update()
        if page_txt.page:
            page_txt.update()

    def _ps_ui_refresh_loop(self) -> None:
        # Refresh UI periodically; packet requests are handled in Client.private_search_list_loop
        while self._ps_running:
            try:
                self._refresh_private_games()
            except Exception:
                pass
            time.sleep(1.5)

    # Actions
    def _on_clear(self, e: ft.ControlEvent) -> None:
        if self.player_id_ref.current:
            self.player_id_ref.current.value = ""
        if self.lobby_name_ref.current:
            self.lobby_name_ref.current.value = ""
        self._validate()
        e.page.update()  # type: ignore

    def _on_join(self, e: ft.ControlEvent, spectate: bool = False) -> None:
        if not self._validate():
            return

        pid = (
            (self.player_id_ref.current.value or "").strip()
            if self.player_id_ref.current
            else ""
        )
        name = (
            (self.lobby_name_ref.current.value or "").strip()
            if self.lobby_name_ref.current
            else ""
        )

        targets = self._selected_clients()
        target_str = (
            "all clients"
            if len(targets) != 1
            else f"{targets[0].client_data.name} ({targets[0].client_data.uid})"
        )

        if pid:
            for client in targets:
                if not client.is_connected:
                    self.app.notify(
                        "Joiner", f"{client.client_data.name} is not connected"
                    )
                    continue
                if spectate:
                    client.send_spectate_request(
                        None, None if not pid.isdigit() else int(pid)
                    )
                else:
                    client.send_enter_game_request(
                        None, None if not pid.isdigit() else int(pid)
                    )
            self.app.notify(
                "Joiner", f"Attempted by Player ID: {pid} on {target_str}"
            )
        elif name:
            for client in targets:
                if not client.is_connected:
                    self.app.notify(
                        "Joiner", f"{client.client_data.name} is not connected"
                    )
                    continue
                if spectate:
                    client.send_spectate_request(name, None)
                else:
                    client.send_enter_game_request(name, None)
            self.app.notify(
                "Joiner", f"Attempted lobby named: {name} on {target_str}"
            )
        else:
            self.app.notify("Joiner", "Provide either Player ID or Lobby name")
        e.page.update()  # type: ignore

    def _on_spectate(self, e: ft.ControlEvent) -> None:
        self._on_join(e, spectate=True)
