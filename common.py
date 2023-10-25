class MyException(Exception):
    pass

def print2dTab(tab: list[list]) -> None:
    for innerTab in tab:
        print(innerTab)
    print("\n")