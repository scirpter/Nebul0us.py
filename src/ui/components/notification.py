import flet as ft
from threading import Thread
from time import sleep
from ui.components.glass import glass_container


def dismiss(ct: ft.Container, notification_list: list[ft.Container]) -> None:
    # Remove from list and refresh the page to reflect change in Column controls
    if ct in notification_list:
        notification_list.remove(ct)
    # Also remove from parent Column if present
    if ct.parent and isinstance(ct.parent, ft.Column):
        try:
            ct.parent.controls.remove(ct)
        except ValueError:
            pass
        ct.parent.update()
    elif ct.page:
        # Fallback: refresh page
        ct.page.update()  # type: ignore


def animate(
    ct: ft.Container,
    progress_bar: ft.ProgressBar,
    notification_list: list[ft.Container],
) -> None:
    # Wait briefly to allow the notification to be added to the page
    # (App.notify appends and updates container asynchronously).
    # Poll for attachment to avoid 'Control must be added to the page first'.
    total_wait = 0.0
    while not ct.page and total_wait < 2.0:
        sleep(0.02)
        total_wait += 0.02

    # Proceed only if attached; otherwise, abort animation gracefully.
    if not ct.page:
        return

    ct.offset = ft.Offset(0, 0)
    ct.update()

    for i in range(100):
        if not progress_bar.page:
            return
        progress_bar.value = 1 - i / 100
        progress_bar.update()
        sleep(0.04)

    ct.offset = ft.Offset(1.09, 0)
    ct.update()
    sleep(0.3)
    dismiss(ct, notification_list)


def craft_notification(
    title: str,
    description: str,
    notification_list: list[ft.Container],
) -> ft.Container:
    progress_bar = ft.ProgressBar(
        1,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
        height=3,
        bar_height=3,
    )

    title_row = ft.Row(
        [
            ft.Container(
                ft.Icon(ft.Icons.NOTIFICATIONS, color=ft.Colors.WHITE, size=16),
                padding=ft.Padding(10, 10, 8, 8),
                bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                border_radius=ft.BorderRadius(10, 10, 10, 10),
            ),
            ft.Text(
                title,
                style=ft.TextStyle(
                    14, weight=ft.FontWeight.W_700, color=ft.Colors.WHITE
                ),
                no_wrap=True,
            ),
            ft.Container(expand=True),
            ft.IconButton(
                ft.Icons.CLOSE,
                icon_size=16,
                icon_color=ft.Colors.WHITE,
                on_click=lambda _: dismiss(c, notification_list),  # type: ignore
                tooltip="Dismiss",
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    body = ft.Text(
        description,
        style=ft.TextStyle(12, color=ft.Colors.WHITE),
    )

    card = glass_container(
        ft.Column([title_row, body, progress_bar], spacing=8, tight=True),
        padding=ft.Padding(14, 12, 14, 12),
        width=280,
    )

    # animate in from the right
    card.offset = ft.Offset(1.1, 0)
    card.animate_offset = ft.Animation(250, ft.AnimationCurve.DECELERATE)

    # Stash into name for access in on_click closure
    c = card

    Thread(
        target=animate, args=(c, progress_bar, notification_list), daemon=True
    ).start()
    return c
