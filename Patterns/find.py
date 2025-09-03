from __future__ import annotations

from binascii import unhexlify
from typing import Literal, TypedDict, Any
from collections import defaultdict
import json
from datetime import datetime, timezone

from barr import ByteArray
from packet_type import PACKET_TYPE


class NotedPacket(TypedDict):
    data: str
    direction: Literal["sent", "recv"]


class Session(TypedDict):
    id: int
    created_at: str
    packets: list[NotedPacket]


class JsonState(TypedDict, total=False):
    last_entered: list[NotedPacket]
    ignored_values: list[str]
    sessions: list[Session]


class Occur:
    __slots__ = ("count", "types", "dirs", "examples")

    def __init__(self) -> None:
        self.count: int = 0
        self.types: set[str] = set()
        self.dirs: set[str] = set()
        # (ptype, dir, pos)
        self.examples: list[tuple[str, str, int]] = []


def get_json_data() -> JsonState:
    """Load data.json into a dict with safe defaults."""
    try:
        with open("data.json", encoding="utf-8") as f:
            loaded: Any = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        loaded = {}
    if not isinstance(loaded, dict):
        data: dict[str, Any] = {}
    else:
        data = loaded  # type: ignore[assignment]
    if not isinstance(data.get("last_entered", None), list):
        data["last_entered"] = []
    if not isinstance(data.get("ignored_values", None), list):
        data["ignored_values"] = []
    if not isinstance(data.get("sessions", None), list):
        data["sessions"] = []
    return data  # type: ignore[return-value]


def add_packets_to_json(packets: list[NotedPacket]) -> None:
    data: JsonState = get_json_data()
    if "last_entered" not in data:
        data["last_entered"] = []
    for packet in packets:
        if packet not in data["last_entered"]:
            data["last_entered"].append(packet)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_session(packets: list[NotedPacket]) -> Session:
    data: JsonState = get_json_data()
    sessions = data.get("sessions", [])
    next_id = (sessions[-1]["id"] + 1) if sessions else 1
    sess: Session = {
        "id": next_id,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "packets": packets,
    }
    sessions.append(sess)
    data["sessions"] = sessions
    data["last_entered"] = packets
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return sess


def clear_json_data() -> None:
    data: JsonState = get_json_data()
    ignored = data.get("ignored_values", [])
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(
            {"last_entered": [], "ignored_values": ignored, "sessions": []}, f, indent=2
        )


def _load_ignored_values() -> set[int]:
    """Parse data.json["ignored_values"] into a set of uint32 ints.
    Accepts values like "00000001" or "0x00000001". Invalid entries are skipped.
    """
    state: JsonState = get_json_data()
    ignored_list = state.get("ignored_values", [])
    out: set[int] = set()
    for item in ignored_list:
        s = item.strip().lower()
        if s.startswith("0x"):
            s = s[2:]
        if len(s) != 8:
            continue
        try:
            out.add(int(s, 16))
        except ValueError:
            pass
    return out


def read(
    packet: str,
    l_: list[tuple[ByteArray, NotedPacket]],
    direction: Literal["sent", "recv"],
) -> None:
    b = ByteArray(unhexlify(packet))
    first_byte: int = b.read_unsigned_byte()
    t_id: PACKET_TYPE | None = PACKET_TYPE.get_type_from_value(first_byte)
    l_.append((b, {"data": packet, "direction": direction}))
    print(
        f"read {len(b.data())} bytes (id: {first_byte}::{t_id.name if t_id else 'noname'})."
    )


def _compute_candidates(
    data: list[tuple[ByteArray, NotedPacket]],
) -> list[tuple[int, Occur]]:
    index: dict[int, Occur] = defaultdict(Occur)
    ignored_vals = _load_ignored_values()

    for b, note in data:
        raw = b.data()
        if not raw or len(raw) < 5:
            continue
        ptype_val = raw[0]
        ptype = PACKET_TYPE.get_type_from_value(ptype_val)
        ptype_name = ptype.name if ptype else f"0x{ptype_val:02X}"
        payload = raw[1:]
        for i in range(0, max(0, len(payload) - 3)):
            val = int.from_bytes(payload[i : i + 4], "big", signed=False)
            if val in ignored_vals or val in (0x00000000, 0xFFFFFFFF):
                continue
            occ = index[val]
            occ.count += 1
            occ.types.add(ptype_name)
            occ.dirs.add(note["direction"])  # "sent" or "recv"
            # Record every occurrence (type, direction, offset)
            occ.examples.append((ptype_name, note["direction"], i + 1))

    candidates: list[tuple[int, Occur]] = [
        (val, occ) for val, occ in index.items() if len(occ.types) >= 2
    ]
    candidates.sort(key=lambda t: (len(t[1].types), t[1].count), reverse=True)
    return candidates


def _packets_to_barr(pkts: list[NotedPacket]) -> list[tuple[ByteArray, NotedPacket]]:
    out: list[tuple[ByteArray, NotedPacket]] = []
    for p in pkts:
        try:
            b = ByteArray(unhexlify(p["data"]))
            out.append((b, p))
        except Exception:
            continue
    return out


def scan_session_tokens(data: list[tuple[ByteArray, NotedPacket]]) -> None:
    """Analyze current input as a session, and validate vs previous session if available."""
    curr_candidates = _compute_candidates(data)

    if not curr_candidates:
        print(
            "No candidate session tokens found (need values reused across multiple packet types)."
        )
        return

    print("\nCandidate session tokens (uint32, big-endian) for current session:")
    for val, occ in curr_candidates:
        types_str = ", ".join(sorted(occ.types))
        dirs_str = "/".join(sorted(occ.dirs))
        print(
            f"- 0x{val:08X}  count={occ.count}  types={{{types_str}}}  dirs={dirs_str}"
        )
        # Show every single occurrence with its packet type and offset
        for ptype_name, direction, pos in sorted(
            occ.examples, key=lambda x: (x[0], x[1], x[2])
        ):
            print(f"    in {ptype_name} ({direction}) at offset {pos}")

    # Validation against previous session (if any)
    state = get_json_data()
    sessions = state.get("sessions", [])
    if len(sessions) >= 2:
        prev = sessions[-2]
        prev_data = _packets_to_barr(prev["packets"])
        prev_candidates = _compute_candidates(prev_data)
        prev_top: list[int] = [v for v, _ in prev_candidates]
        curr_top: list[int] = [v for v, _ in curr_candidates]

        print("\nValidation vs previous session:")
        max_len = max(len(prev_top), len(curr_top))
        for i in range(max_len):
            rank = i + 1
            pv = prev_top[i] if i < len(prev_top) else None
            cv = curr_top[i] if i < len(curr_top) else None
            if pv is None and cv is not None:
                print(f"- Rank {rank} new: 0x{cv:08X}")
            elif pv is not None and cv is None:
                ...
                # print(f"- Rank {rank} dropped: 0x{pv:08X}")
            elif pv == cv:
                print(
                    f"- Rank {rank} unchanged: 0x{cv:08X} (may be constant, less likely a per-session token)"
                )
            else:
                # both present and different
                print(f"- Rank {rank} changed: 0x{pv:08X} -> 0x{cv:08X} (validated)")

        # End-of-run grouped summary with classification and locations
        curr_map = dict(curr_candidates)
        prev_map = dict(prev_candidates)

        constants = sorted(
            curr_map.keys() & prev_map.keys(),
            key=lambda v: (len(curr_map[v].types), curr_map[v].count),
            reverse=True,
        )
        dynamic_new = sorted(
            curr_map.keys() - prev_map.keys(),
            key=lambda v: (len(curr_map[v].types), curr_map[v].count),
            reverse=True,
        )
        dynamic_dropped = sorted(
            prev_map.keys() - curr_map.keys(),
            key=lambda v: (len(prev_map[v].types), prev_map[v].count),
            reverse=True,
        )

        def _print_occ(val: int, occ: Occur, label: str) -> None:
            types_str = ", ".join(sorted(occ.types))
            dirs_str = "/".join(sorted(occ.dirs))
            print(
                f"- 0x{val:08X}  {label}  count={occ.count}  types={{{types_str}}}  dirs={dirs_str}"
            )
            for ptype_name, direction, pos in sorted(
                occ.examples, key=lambda x: (x[0], x[1], x[2])
            ):
                print(f"    in {ptype_name} ({direction}) at offset {pos}")

        print("\nSummary of tokens by status:")
        print(f"  Constants across sessions ({len(constants)}):")
        for v in constants:
            _print_occ(v, curr_map[v], "constant")
        print(f"  Dynamic – new this session ({len(dynamic_new)}):")
        for v in dynamic_new:
            _print_occ(v, curr_map[v], "dynamic (new)")
        print(f"  Dynamic – dropped since previous ({len(dynamic_dropped)}):")
        for v in dynamic_dropped:
            _print_occ(v, prev_map[v], "dynamic (dropped)")
    else:
        print(
            "\nNo previous session to validate against yet. Add another round to compare."
        )
        # With no previous session, still provide a concise end-of-run list
        curr_map = dict(curr_candidates)
        print(
            "\nSummary of tokens (no previous session for dynamic/constant classification):"
        )
        for v in curr_map:
            occ = curr_map[v]
            types_str = ", ".join(sorted(occ.types))
            dirs_str = "/".join(sorted(occ.dirs))
            print(
                f"- 0x{v:08X}  count={occ.count}  types={{{types_str}}}  dirs={dirs_str}"
            )
            for ptype_name, direction, pos in sorted(
                occ.examples, key=lambda x: (x[0], x[1], x[2])
            ):
                print(f"    in {ptype_name} ({direction}) at offset {pos}")


def main() -> None:
    data: list[tuple[ByteArray, NotedPacket]] = []
    e: str = input("reuse json? (n): ")

    if e.lower() == "n":
        # New session (round)
        entered: list[NotedPacket] = []
        while True:
            x: str = input("enter hex string (e.g. d34db3efR/S): ")
            if not x:
                break
            suffix = x[-1].lower()
            if suffix not in ("s", "r"):
                print("  Please end with 'S' or 'R' to mark direction.")
                continue
            direction: Literal["sent", "recv"] = "sent" if suffix == "s" else "recv"
            packet: str = x[:-1]
            # Validate hex
            try:
                _ = unhexlify(packet)
            except Exception:
                print("  Invalid hex; try again.")
                continue
            read(packet, data, direction)
            entered.append({"data": packet, "direction": direction})

        if entered:
            add_session(entered)
        else:
            print("No packets entered; nothing saved.")

    else:
        # Reuse last session
        json_data: JsonState = get_json_data()
        # Prefer the last session if present; fallback to legacy last_entered
        sessions = json_data.get("sessions", [])
        if sessions:
            pkts = sessions[-1]["packets"]
        else:
            pkts = json_data.get("last_entered", [])
        for dataset in pkts:
            read(dataset["data"], data, dataset["direction"])

    scan_session_tokens(data)


if __name__ == "__main__":
    main()
