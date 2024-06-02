from base.app import App
import os
import flet as ft
from ui.abuse import AbuseTab
from ui.auth import AuthTab
from ui.bin import BinTab
from ui.bots import BotsTab
from ui.devlogs import DevLogsTab
from ui.general_settings import GeneralSettingsTab
from ui.packet_log import PacketLogsTab
from ui.proxies import ProxiesTab
from ui.theme import ThemeTab


def main(page: ft.Page) -> None:
    page.title = "Nebul0us V2"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = app.statery["theme"]["background_color_hex"]
    page.padding = 0
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.TERTIARY,
        color_scheme=ft.ColorScheme(
            primary=app.statery["theme"]["primary_color_hex"],
            secondary=app.statery["theme"]["secondary_color_hex"],
            tertiary=app.statery["theme"]["tertiary_color_hex"],
        ),
    )
    app.page = page

    tabs: list[ft.Tab] = [
        DevLogsTab(app),
        AuthTab(app),
        BotsTab(app),
        AbuseTab(app),
        GeneralSettingsTab(app),
        ThemeTab(app),
        PacketLogsTab(app),
        ProxiesTab(app),
        BinTab(app),
    ]

    app.statery["background_image_container"] = ft.Container(
        image_src=app.statery["theme"]["background_image_url"],
        image_opacity=app.statery["theme"]["background_image_opacity"],
        image_fit=ft.ImageFit.COVER,
        expand=True,
        content=ft.Container(
            ft.Tabs(
                selected_index=2,
                animation_duration=300,
                tabs=tabs,
                height=page.height,
                width=page.width,
                tab_alignment=ft.TabAlignment.CENTER,
            ),
            padding=ft.Padding(10, 0, 10, 0),
        ),
    )

    app.statery["notification_container"] = ft.Container(
        ft.Column(
            app.statery["notifications"],  # type: ignore
            scroll=ft.ScrollMode.ALWAYS,
            height=100 * len(app.statery["notifications"]),
        ),
        width=200,
        height=page.height,
        right=20,
        margin=ft.Margin(0, 10, 0, 0),
    )

    st = ft.Stack(
        [
            app.statery["background_image_container"],
            app.statery["notification_container"],
        ]
    )
    page.add(st)

    app.notify("Welcome home", "Thanks for using Nebul0us V2!")
    DevLogsTab.log("App started", "info")


os.system("cls" if os.name == "nt" else "clear")
print("")
app: App = App()
ft.app(target=main)
