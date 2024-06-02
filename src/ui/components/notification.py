import flet as ft
from threading import Thread
from time import sleep


def dismiss(ct: ft.Container, notification_list: list[ft.Container]) -> None:
    notification_list.remove(ct)
    ct.parent.height = 100 * len(notification_list)  # type: ignore
    ct.parent.update()


def animate(
    ct: ft.Container,
    progress_bar: ft.ProgressBar,
    notification_list: list[ft.Container],
) -> None:
    sleep(0.1)
    ct.parent.height = 100 * len(notification_list)  # type: ignore
    ct.offset = ft.Offset(0, 0)
    ct.parent.update()

    for i in range(100):
        if not progress_bar.page:
            return
        progress_bar.value = 1 - i / 100
        progress_bar.update()
        sleep(0.04)

    ct.offset = ft.Offset(1.09, 0)
    ct.parent.update()
    sleep(0.3)
    notification_list.remove(ct)
    ct.parent.height = 100 * len(notification_list)  # type: ignore
    ct.parent.update()


def craft_notification(
    title: str,
    description: str,
    notification_list: list[ft.Container],
) -> ft.Container:
    progress_bar = ft.ProgressBar(1)

    c = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            ft.icons.CANCEL,
                            on_click=lambda _: dismiss(c, notification_list),  # type: ignore
                        ),
                        ft.Text(
                            title,
                            style=ft.TextStyle(13, weight=ft.FontWeight.BOLD),
                        ),
                    ],
                    spacing=0,
                ),
                ft.Container(
                    ft.Text(description),
                    padding=ft.Padding(5, 0, 5, 2),
                ),
                progress_bar,
            ],
            spacing=0,
        ),
        border=ft.Border(
            ft.BorderSide(2, ft.colors.GREY_800),
            ft.BorderSide(2, ft.colors.GREY_800),
            ft.BorderSide(2, ft.colors.GREY_800),
            ft.BorderSide(2, ft.colors.GREY_800),
        ),
        border_radius=ft.BorderRadius(10, 10, 10, 10),
        offset=ft.Offset(1.09, 0),
        animate_offset=ft.Animation(300),
    )
    Thread(target=animate, args=(c, progress_bar, notification_list)).start()
    return c
