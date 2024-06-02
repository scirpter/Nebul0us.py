class Tab:
    a = "a"

    def __init__(self) -> None:
        Tab.a = "b"


x = Tab()

print(Tab.a)  # why doesnt this return "b"?
