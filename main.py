from src.network import AS, BGP
from typing import Callable


def main() -> None:
    as1 = AS(
        id="AS1",
        nodes=["1a", "1b", "1c", "1d"],
        gateway_nodes=["1c"],
        edges=[
            ("1a", "1b", 5),
            ("1a", "1d", 3),
            ("1a", "1c", 1),
            ("1b", "1d", 8),
            ("1b", "1c", 4),
            ("1d", "1c", 2),
        ],
    )

    as2 = AS(
        id="AS2",
        nodes=["2a", "2b", "2c", "2d"],
        gateway_nodes=["2a", "2c"],
        edges=[
            ("2a", "2b", 5),
            ("2a", "2d", 4),
            ("2a", "2c", 7),
            ("2b", "2d", 4),
            ("2b", "2c", 3),
            ("2d", "2c", 5),
        ],
    )

    as3 = AS(
        id="AS3",
        nodes=["3a", "3b", "3c", "3d"],
        gateway_nodes=["3a", "3c"],
        edges=[
            ("3a", "3b", 1),
            ("3a", "3d", 6),
            ("3a", "3c", 10),
            ("3b", "3d", 7),
            ("3b", "3c", 5),
            ("3d", "3c", 8),
        ],
    )

    bgp1 = BGP("BGP1", [as1, as2, as3], [(as1, as2, 12), (as2, as3, 9), (as1, as3, 3)])

    print(bgp1)


def print_bgp(bgp: BGP) -> Callable[[], None]:
    def wrapper():
        print("\033[H\033[xJ", end="")
        print(bgp)

    return wrapper


if __name__ == "__main__":
    main()
