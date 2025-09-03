from __future__ import annotations
import threading
import time
import flet as ft
from base.app import App
from game.models.client.client import Client
from game.models.world import World


class WorldDBGTab(ft.Tab):
    def __init__(self, app: App) -> None:
        self.app = app
        self._auto_thread: threading.Thread | None = None
        self._auto_running = False
        self._last_scroll_ts: float = 0.0

        # Controls
        self.client_dd = ft.Dropdown(
            label="Client",
            options=[
                ft.dropdown.Option(
                    str(c.client_data.uid),
                    f"{c.client_data.name} ({c.client_data.uid})",
                )
                for c in self.app.clients
            ],
            on_change=self._on_change,
            width=320,
        )
        self.type_dd = ft.Dropdown(
            label="Object type",
            options=[
                ft.dropdown.Option("players", "Players"),
                ft.dropdown.Option("holes", "Holes"),
            ],
            value="players",
            on_change=self._on_change,
            width=180,
        )
        self.auto_sw = ft.Switch(
            label="Auto refresh", value=True, on_change=self._on_auto_toggle
        )
        self.refresh_btn = ft.IconButton(
            icon=ft.Icons.REFRESH, tooltip="Refresh", on_click=self._refresh
        )
        self.clients_btn = ft.IconButton(
            icon=ft.Icons.PERSON_SEARCH,
            tooltip="Reload clients",
            on_click=self._reload_clients,
        )

        # Scrollable data area: reuse this ListView/Row to avoid scroll reset on refresh
        self.table_row = ft.Row(scroll=ft.ScrollMode.ALWAYS)
        self.table_list = ft.ListView(
            controls=[self.table_row],
            expand=True,
            auto_scroll=False,
            spacing=0,
            padding=0,
            on_scroll=self._on_list_scroll,
            on_scroll_interval=100,
        )
        self.table_container = ft.Container(
            content=self.table_list, expand=True
        )

        super().__init__(
            text="WorldDBG",
            icon=ft.Icons.PUBLIC,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.client_dd,
                            self.type_dd,
                            self.auto_sw,
                            self.refresh_btn,
                            self.clients_btn,
                        ],
                        wrap=True,
                        spacing=14,
                    ),
                    self.table_container,
                ],
                expand=True,
                spacing=12,
            ),
        )

        # Start auto refresh once attached
        self._start_auto()

    # Control events
    def _on_change(self, _: ft.ControlEvent) -> None:
        self._refresh(None)

    def _on_auto_toggle(self, _: ft.ControlEvent) -> None:
        if self.auto_sw.value:
            self._start_auto()
        else:
            self._stop_auto()

    def _on_list_scroll(self, _: ft.OnScrollEvent) -> None:
        # Remember user scroll time; skip auto refresh briefly afterwards
        self._last_scroll_ts = time.time()

    def _reload_clients(self, _: ft.ControlEvent) -> None:
        # Rebuild client list options from app state
        self.client_dd.options = [
            ft.dropdown.Option(
                str(c.client_data.uid),
                f"{c.client_data.name} ({c.client_data.uid})",
            )
            for c in self.app.clients
        ]
        self.client_dd.update()

    # Auto refresh loop
    def _start_auto(self) -> None:
        if self._auto_running:
            return
        self._auto_running = True

        def loop() -> None:
            while self._auto_running:
                # Avoid updating if not attached
                if self.page:
                    # Skip refresh if user recently scrolled (within ~0.8s)
                    if time.time() - self._last_scroll_ts < 0.8:
                        time.sleep(0.1)
                        continue
                    try:
                        self._refresh(None)
                    except Exception:
                        pass
                time.sleep(0.5)

        self._auto_thread = threading.Thread(target=loop, daemon=True)
        self._auto_thread.start()

    def _stop_auto(self) -> None:
        self._auto_running = False
        self._auto_thread = None

    # Helpers
    def _selected_client(self) -> Client | None:
        if not self.client_dd.value:
            return None
        try:
            uid = int(self.client_dd.value)
        except ValueError:
            return None
        for c in self.app.clients:
            if c.client_data.uid == uid:
                return c
        return None

    def _refresh(self, _: ft.ControlEvent | None) -> None:
        client = self._selected_client()
        if not client or not client.client_data.world:
            self.table_row.controls = [
                ft.Container(
                    ft.Text(
                        "Pick a client to view world data", color=ft.Colors.GREY
                    ),
                    padding=16,
                )
            ]
            self.table_row.update()
            return

        world = client.client_data.world
        ty = self.type_dd.value

        if ty == "players":
            rows, columns = self._build_players(world)
        elif ty == "holes":
            rows, columns = self._build_holes(world)
        else:
            rows, columns = [], []

        if not columns:
            self.table_row.controls = [
                ft.Container(ft.Text("No data available."), padding=16)
            ]
        else:
            table = ft.DataTable(
                columns=columns,
                rows=rows,
                heading_row_color=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                data_row_min_height=38,
                divider_thickness=0.5,
            )
            self.table_row.controls = [table]
        self.table_row.update()

    def _build_players(
        self, world: World
    ) -> tuple[list[ft.DataRow], list[ft.DataColumn]]:
        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Mass")),
            ft.DataColumn(ft.Text("Blobs")),
            ft.DataColumn(ft.Text("Avg X")),
            ft.DataColumn(ft.Text("Avg Y")),
        ]
        rows: list[ft.DataRow] = []
        for pid, p in world.players.copy().items():
            try:
                avg = p.get_avg_pos()
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(pid))),
                            ft.DataCell(ft.Text(p.name)),
                            ft.DataCell(ft.Text(f"{p.get_mass():.1f}")),
                            ft.DataCell(ft.Text(str(len(p.blobs)))),
                            ft.DataCell(
                                ft.Text(f"{avg.x:.1f}" if avg else "-")
                            ),
                            ft.DataCell(
                                ft.Text(f"{avg.y:.1f}" if avg else "-")
                            ),
                        ]
                    )
                )
            except Exception:
                continue
        return rows, columns

    def _build_holes(
        self, world: World
    ) -> tuple[list[ft.DataRow], list[ft.DataColumn]]:
        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Type")),
            ft.DataColumn(ft.Text("Mass")),
            ft.DataColumn(ft.Text("X")),
            ft.DataColumn(ft.Text("Y")),
        ]
        rows: list[ft.DataRow] = []
        for hid, h in world.holes.copy().items():
            try:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(hid))),
                            ft.DataCell(
                                ft.Text(
                                    h.type.name
                                    if hasattr(h.type, "name")
                                    else str(h.type)
                                )
                            ),
                            ft.DataCell(ft.Text(f"{h.mass:.1f}")),
                            ft.DataCell(ft.Text(f"{h.pos.x:.1f}")),
                            ft.DataCell(ft.Text(f"{h.pos.y:.1f}")),
                        ]
                    )
                )
            except Exception:
                continue
        return rows, columns
