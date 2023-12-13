from base.app import App
import logging
import os
from rich.logging import RichHandler

from helpers.plugins import ScriptEvent


def main() -> None:
    app.dispatch(ScriptEvent.CALLBACK, "install", 90, 100)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )

    app: App = App().register_plugins()
    main()
