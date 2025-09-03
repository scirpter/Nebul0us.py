import json
import pathlib
from typing import Any, TypedDict
import flet as ft
from game.enums.profile_visibility import PROFILE_VISIBILITY


class PerClientSettings(TypedDict):
    client_uid: int
    player_name: str
    login_ticket: str
    profile_visibility: str
    idle_keep_alive_ms: int
    active_keep_alive_ms: int


def get_default_client_settings(
    uid: int, name: str, ticket: str
) -> PerClientSettings:
    return {
        "client_uid": uid,
        "player_name": name,
        "login_ticket": ticket,
        "profile_visibility": PROFILE_VISIBILITY.ONLINE.name,
        "idle_keep_alive_ms": 502,
        "active_keep_alive_ms": 52,
    }


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


class GeneralSettings(TypedDict):
    detect_moderators: bool
    auto_save_config: bool
    trace_packets: bool


class Cache(TypedDict):
    notification_container: ft.Container
    notification_column: ft.Column
    background_image_container: ft.Container
    notifications: list[ft.Container]


class AppStates(TypedDict):
    license_key: str
    cache: Cache
    theme: Theme
    bin_text: str
    client_settings: list[PerClientSettings]
    general_settings: GeneralSettings


def ensure_integrity(config: dict[str, Any]) -> dict[str, Any]:
    if not config.get("license_key"):
        config["license_key"] = ""

    if not config.get("client_settings"):
        config["client_settings"] = []

    if not config.get("cache"):
        config["cache"] = {}

    if not config["cache"].get("notifications"):  # type: ignore
        config["cache"]["notifications"] = []

    if not config.get("theme"):
        config["theme"] = {}

    if not config["theme"].get("background_color_hex"):  # type: ignore
        config["theme"]["background_color_hex"] = "#171717"

    if not config["theme"].get("primary_color_hex"):  # type: ignore
        config["theme"]["primary_color_hex"] = "#ffffff"

    if not config["theme"].get("secondary_color_hex"):  # type: ignore
        config["theme"]["secondary_color_hex"] = "#7c4dff"

    if not config["theme"].get("tertiary_color_hex"):  # type: ignore
        config["theme"]["tertiary_color_hex"] = "#7c4dff"

    if not config["theme"].get("background_image_url"):  # type: ignore
        config["theme"]["background_image_url"] = ""

    if not config["theme"].get("background_image_opacity"):  # type: ignore
        config["theme"]["background_image_opacity"] = 1

    if not config.get("bin_text"):
        config["bin_text"] = (
            "Write something here that you need to save for later."
        )

    if not config.get("general_settings"):
        config["general_settings"] = {}

    if not config["general_settings"].get("detect_moderators"):  # type: ignore
        config["general_settings"]["detect_moderators"] = False

    if not config["general_settings"].get("auto_save_config"):  # type: ignore
        config["general_settings"]["auto_save_config"] = True

    if not config["general_settings"].get("trace_packets"):  # type: ignore
        config["general_settings"]["trace_packets"] = False

    return config


def ensure_client_config_integrity(
    client_settings: PerClientSettings,
) -> PerClientSettings:
    if not client_settings.get("idle_keep_alive_ms"):
        client_settings["idle_keep_alive_ms"] = 502

    if not client_settings.get("active_keep_alive_ms"):
        client_settings["active_keep_alive_ms"] = 52

    if not client_settings.get("profile_visibility"):
        client_settings["profile_visibility"] = PROFILE_VISIBILITY.ONLINE.name

    return client_settings


def save_config(states: AppStates) -> None:
    with open("config.json", "w+") as f:
        config: AppStates = states.copy()
        del config["cache"]  # type: ignore
        f.write(json.dumps(config, indent=4))


def load_config() -> dict[str, Any]:
    if not pathlib.Path("config.json").exists():
        return {}

    with open("config.json") as f:
        try:
            return json.loads(f.read())
        except json.JSONDecodeError:
            return {}
