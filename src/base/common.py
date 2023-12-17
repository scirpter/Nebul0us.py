import platform


# platform.machine(), bin file name
mobile_arches: dict[str, str] = {
    "aarch64": "arm64-v8a",
    "armeabi-v7a": "x86_64",
    "arm": "armeabi-v7a",
    "i686": "x86",
}


def get_local_arch() -> tuple[str, bool]:
    """Returns the local architecture and whether or not it's mobile"""
    return platform.machine(), platform.machine() in mobile_arches
