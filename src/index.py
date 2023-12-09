from base.app import App


def main() -> None:
    ...


if __name__ == "__main__":
    app: App = App().register_plugins()
    main()
