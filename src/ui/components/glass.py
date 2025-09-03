import flet as ft


def glass_container(
    content: ft.Control,
    *,
    padding: ft.Padding | None = None,
    margin: ft.Margin | None = None,
    width: float | None = None,
    height: float | None = None,
    expand: int | bool | None = None,
) -> ft.Container:
    return ft.Container(
        content=content,
        width=width,
        height=height,
        expand=expand,
        padding=padding or ft.Padding(16, 16, 16, 16),
        margin=margin,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
        border=ft.Border(
            ft.BorderSide(1, ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
            ft.BorderSide(1, ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
            ft.BorderSide(1, ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
            ft.BorderSide(1, ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
        ),
        border_radius=ft.BorderRadius(18, 18, 18, 18),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(0, 8),
        ),
    )
