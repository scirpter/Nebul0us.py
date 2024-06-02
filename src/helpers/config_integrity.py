import json
import pathlib
from typing import Any, TypedDict
import flet as ft


class Notification(TypedDict):
    title: str
    message: str


class Theme(TypedDict):
    background_color_hex: str
    primary_color_hex: str
    secondary_color_hex: str
    tertiary_color_hex: str
    background_image_url: str
    background_image_opacity: float


class AppStatery(TypedDict):
    license_key: str
    notifications: list[ft.Container]
    background_image_container: ft.Container
    notification_container: ft.Container
    theme: Theme
    bin_text: str


def ensure_integrity(config: dict[str, Any]) -> dict[str, Any]:
    if not config.get("license_key"):
        config["license_key"] = ""

    if not config.get("notifications"):
        config["notifications"] = []

    if not config.get("theme"):
        config["theme"] = {}
    if not config["theme"].get("background_color_hex"):
        config["theme"]["background_color_hex"] = "#171717"
    if not config["theme"].get("primary_color_hex"):
        config["theme"]["primary_color_hex"] = "#ffffff"
    if not config["theme"].get("secondary_color_hex"):
        config["theme"]["secondary_color_hex"] = "#7c4dff"
    if not config["theme"].get("tertiary_color_hex"):
        config["theme"]["tertiary_color_hex"] = "#7c4dff"
    if not config["theme"].get("background_image_url"):
        config["theme"]["background_image_url"] = ""
    if not config["theme"].get("background_image_opacity"):
        config["theme"]["background_image_opacity"] = 1

    if not config.get("bin_text"):
        config["bin_text"] = "Write something here that you need to save for later."

    return config


def save_config(statery: AppStatery) -> None:
    with open("config.json", "w+") as f:
        # remove notifications
        config: AppStatery = statery.copy()
        config["notifications"] = []
        config["background_image_container"] = None  # type: ignore
        config["notification_container"] = None  # type: ignore
        f.write(json.dumps(config))


def load_config() -> dict[str, Any]:
    # creater if not exists
    if not pathlib.Path("config.json").exists():
        return {}

    with open("config.json") as f:
        try:
            return json.loads(f.read())
        except json.JSONDecodeError:
            return {}
