from base.app import App
import os
import flet as ft
from ui.abuse import AbuseTab
from ui.auth import AuthTab
from ui.bin import BinTab
from ui.bots import BotsTab
from ui.devlogs import DevLogs
from ui.general_settings import GeneralSettingsTab
from ui.theme import ThemeTab
from ui.components.glass import glass_container
from ui.world_dbg import WorldDBGTab
from ui.lobbies import LobbiesTab


def main(page: ft.Page) -> None:
    page.title = "2oh"
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = None
    page.theme = ft.Theme(
        color_scheme_seed=app.states["theme"]["tertiary_color_hex"],
        color_scheme=ft.ColorScheme(
            primary=app.states["theme"]["primary_color_hex"],
            secondary=app.states["theme"]["secondary_color_hex"],
            tertiary=app.states["theme"]["tertiary_color_hex"],
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
        use_material3=True,
    )
    app.page = page

    tabs: list[ft.Tab] = [
        DevLogs(app),
        AuthTab(app),
        LobbiesTab(app),
        BotsTab(app),
        AbuseTab(app),
        GeneralSettingsTab(app),
        ThemeTab(app),
        WorldDBGTab(app),
        BinTab(app),
    ]

    gradient_backdrop = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[
                ft.Colors.with_opacity(0.9, ft.Colors.BLACK),
                ft.Colors.with_opacity(0.9, ft.Colors.BLACK),
            ],
        ),
    )

    tabs_control = ft.Tabs(
        selected_index=2,
        animation_duration=300,
        tabs=tabs,
        expand=1,
        tab_alignment=ft.TabAlignment.CENTER,
        indicator_tab_size=True,
        divider_color=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
    )

    content_wrapper = ft.Container(
        content=glass_container(
            tabs_control,
            padding=ft.Padding(8, 8, 8, 8),
            expand=True,
        ),
        padding=ft.Padding(12, 12, 12, 12),
        expand=True,
    )

    app.states["cache"]["background_image_container"] = ft.Container(
        image=ft.DecorationImage(
            app.states["theme"]["background_image_url"],
            opacity=app.states["theme"]["background_image_opacity"],
            fit=ft.ImageFit.COVER,
        ),
        expand=True,
        content=ft.Stack([gradient_backdrop, content_wrapper]),
    )

    app.states["cache"]["notification_column"] = ft.Column(
        app.states["cache"]["notifications"],  # type: ignore[list-item]
        spacing=6,
        scroll=ft.ScrollMode.AUTO,
    )

    app.states["cache"]["notification_container"] = ft.Container(
        content=app.states["cache"]["notification_column"],  # type: ignore
        width=320,
        right=24,
        top=18,
        margin=ft.Margin(0, 10, 0, 0),
    )

    st = ft.Stack(
        [
            app.states["cache"]["background_image_container"],
            app.states["cache"]["notification_container"],
        ],
        expand=True,
    )
    page.add(st)

    app.notify("Welcome Home", "Thanks for using 2oh!")
    app.devlog("App started", "info")


os.system("cls" if os.name == "nt" else "clear")
print("")
app: App = App(DevLogs.log)
ft.app(target=main)
