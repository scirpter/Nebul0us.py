from __future__ import annotations
from binascii import hexlify
from datetime import datetime, timedelta

import pytz
from game.api import GetRPGResetToken, JDKaYIIScQ
from time import sleep
from typing import TYPE_CHECKING, Any, Callable
from game.enums.rpg_skilltree import RPG_SKILLTREE_UPGRADE
from game.models.client.client_data import ClientData
from game.models.client.functions import functions
from game.models.client.options_data import OptionsData
from game.models.client.player_data import PlayerData
from game.models.client.private_search_list import PrivateSearchList
from game.models.client.wardrobe import Wardrobe
from game.models.client.control_data import ControlData
import socket
from game.packets.connect_request_3 import CONNECT_REQUEST_3
from game.packets.control import CONTROL
from game.packets.create_skill_tree_upgrade import CREATE_SKILL_TREE_UPGRADE
from game.packets.disconnect import DISCONNECT
from game.packets.enter_game_request import ENTER_GAME_REQUEST
from game.packets.join_request import JOIN_REQUEST
from game.packets.keep_alive import KEEP_ALIVE
from game.packets.packet import Packet
from game.packets.ping import PING
from game.packets.private_search_list_request import PRIVATE_SEARCH_LIST_REQUEST
from game.packets.spectate_game_request import SPECTATE_GAME_REQUEST
from helpers.common import get_packet_class_by_id
from helpers.config_integrity import PerClientSettings
from threading import Thread
from game.enums import GAME_MODE


if TYPE_CHECKING:
    from base.app import App
    from game.packets.packet import Packet


class Client:
    def __init__(self, app: App, uid: int, name: str, ticket: str) -> None:
        self.app: App = app
        self.settings: PerClientSettings = (
            self.app.fetch_client_settings_from_uid(uid, name, ticket)
        )
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.is_connected: bool = False
        self.wardrobe = Wardrobe()
        self.control_data = ControlData()
        self.client_data = ClientData(self)
        self.player_data = PlayerData(self)
        self.options_data = OptionsData()
        self.private_search_list = PrivateSearchList()
        self.last_packet_received_at: None | datetime = None
        self.__sock_connected = False

    def setup_loops(self) -> None:
        loops: list[Callable[[], None]] = [
            self.recv_packet_loop,
            self.check_desync_loop,
            self.keep_alive_loop,
            self.functions_loop,
            self.private_search_list_loop,
        ]
        for loop in loops:
            Thread(target=loop).start()

    def connect(
        self,
        region: str,
        game_mode: GAME_MODE,
        connect_in_private_search: bool,
        mayhem: bool,
    ) -> None | Exception:
        verify: dict[Any, Any] | Exception = JDKaYIIScQ(
            self.client_data.login_ticket, region
        ).execute()
        if isinstance(verify, Exception):
            return Exception(
                f"{self.client_data.name} failed to verify connection: {verify} :?"
            )
        elif verify["IP"] == "127.0.0.1":
            return Exception(
                "Failed to verify captcha. Please reconnect using real device.",
            )

        self.app.devlog(
            f"{self.client_data.name} trying to connect to {verify['IP']}:{verify['PortA']}",
            "info",
        )
        self.client_data.server_ip = verify["IP"]
        self.client_data.server_port = verify["PortA"]
        print(verify)

        self.app.notify(
            "Lobby",
            f"{self.client_data.name} connecting to {self.client_data.server_ip}:{self.client_data.server_port}...",
        )

        self.sock.connect(
            (self.client_data.server_ip, self.client_data.server_port)
        )
        self.__sock_connected = True
        self.send_packet(PING(self))

        for x in range(6):
            if self.client_data.pingpong_token:
                self.send_packet(
                    CONNECT_REQUEST_3(
                        self,
                        game_mode,
                        connect_in_private_search,
                        mayhem,
                        verify["RezPlEVBeW"],
                        self.client_data.pingpong_token,
                        verify["Nonce"],
                    )
                )
                break
            if x == 5 and not self.is_connected:
                self.client_data.server_ip = None
                self.client_data.server_port = None
                return Exception(
                    f"{self.client_data.name} timed out connecting to {self.client_data.server_ip}. :|",
                )
            sleep(1)

    def send_packet(self, packet: Packet) -> None:
        if not self.client_data.server_ip:
            return
        self.sock.send(packet.write())

    def functions_loop(self) -> None:
        last_control_tick: int | None = None
        while self in self.app.clients:
            if not self.is_connected:
                sleep(0.2)
                continue

            player = self.client_data.world.get_player_by_name(
                self.client_data.name
            )
            if (
                player and (avg_pos := player.get_avg_pos())
            ):  # private lobby search list is gonna be outdated since were not receiving any results anymore. clear list
                if self.private_search_list.entries:
                    self.private_search_list.reset()
                functions(self, player, avg_pos)
            else:
                self.control_data.reset()

            if self.client_data.world.control_tick != last_control_tick:
                self.send_packet(CONTROL(self))
                last_control_tick = self.client_data.world.control_tick

            sleep(0.01)

    def is_idle(self) -> bool:
        return (
            self.control_data.speed == 0
            and not self.control_data.do_eject
            and not self.control_data.do_item_drop
            and not self.control_data.do_split
        )

    def check_desync_loop(self) -> None:
        while self in self.app.clients:
            if (
                self.last_packet_received_at
                and datetime.now(pytz.utc) - self.last_packet_received_at
                > timedelta(seconds=5)
                and self.client_data.cr_tokens_present()
            ):  # desync
                self.is_connected = False
                self.app.notify(
                    "Session", f"Bot {self.client_data.name} desynced"
                )
                self.last_packet_received_at = None
                self.disconnect(True)
            elif (
                self.last_packet_received_at
                and self.client_data.cr_tokens_present()
            ):
                self.is_connected = True
            elif not self.client_data.cr_tokens_present():
                self.is_connected = False
            sleep(0.3)

    def keep_alive_loop(self) -> None:
        while self in self.app.clients:
            if not self.is_connected:
                sleep(0.1)
                continue

            self.send_packet(KEEP_ALIVE(self))
            if not self.is_idle():
                sleep(self.settings["active_keep_alive_ms"] / 1000)
                continue

            sleep(self.settings["idle_keep_alive_ms"] / 1000)

    def recv_packet_loop(self) -> None:
        while self in self.app.clients:
            if not self.client_data.server_ip or not self.__sock_connected:
                sleep(0.1)
                continue
            packet: bytes = self.sock.recv(1024 * 4)
            self.last_packet_received_at = datetime.now(pytz.utc)
            packet_id: int = packet[0]
            klass: type[Packet] | bool = get_packet_class_by_id(packet_id)
            if isinstance(klass, bool):
                if not klass:
                    self.app.notify(
                        "DEBUG",
                        f"Unrecognized packet {hexlify(packet_id.to_bytes(1, 'big')).decode()}",
                    )
                    self.app.devlog(
                        f"Unrecognized packet {hexlify(packet_id.to_bytes(1, 'big')).decode()}",
                        "warning",
                    )
                continue

            klass(self, packet)  # type: ignore

    def disconnect(self, desynced: bool = False) -> None:
        if not desynced:
            self.send_packet(DISCONNECT(self))
        self.client_data.reset_all_tokens()
        self.client_data.world.reset()
        self.private_search_list.reset()
        self.is_connected = False
        self.__sock_connected = False

    def start_playing(self) -> None:
        self.send_packet(JOIN_REQUEST(self))

    def do_respawn_after_death(self) -> None:
        """smart respawn. waits for all holes to load back before spawning."""

        def non_blocking() -> None:
            while True:
                holes = self.client_data.world.holes.copy().values()
                holes_allive = [hole for hole in holes if not hole.is_dead()]
                if len(holes_allive) == len(holes):
                    self.start_playing()
                    break
                sleep(0.01)

        Thread(target=non_blocking).start()

    def send_spectate_request(
        self, lobby_name: str | None = None, account_id: int | None = None
    ) -> None:
        if not lobby_name and not account_id:
            return
        self.send_packet(SPECTATE_GAME_REQUEST(self, lobby_name, account_id))

    def send_enter_game_request(
        self, lobby_name: str | None = None, account_id: int | None = None
    ) -> None:
        if not lobby_name and not account_id:
            return
        self.send_packet(ENTER_GAME_REQUEST(self, lobby_name, account_id))

    def request_private_search_list(self) -> None:
        if not self.private_search_list.token:
            return
        self.send_packet(PRIVATE_SEARCH_LIST_REQUEST(self))

    def private_search_list_loop(self) -> None:
        """Periodically request private search list results when token is present."""
        while self in self.app.clients:
            if not self.is_connected:
                sleep(0.2)
                continue

            if self.private_search_list.token:
                self.request_private_search_list()
                sleep(1.5)
                continue

            sleep(0.3)

    def upgrade_skill_tree(
        self, upgrade: RPG_SKILLTREE_UPGRADE, reset: bool = False
    ) -> None:
        reset_token: str | None = None
        if reset:
            response = GetRPGResetToken(self.client_data.login_ticket).execute()
            if isinstance(response, Exception):
                self.app.notify(
                    "API",
                    f"{self.client_data.name} failed to get reset token: {response}",
                )
                return

            reset_token = response.get("Token")
        self.send_packet(CREATE_SKILL_TREE_UPGRADE(self, upgrade, reset_token))
