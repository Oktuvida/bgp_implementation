from src.network import AS, BGP
from src.graph import Graph
from src.utils import Globals, plotlive
from signal import signal, SIGINT
from time import sleep
from apscheduler.schedulers.base import EVENT_SCHEDULER_START


def signalHandler(signal_received: int, frame) -> None:
    if signal_received == SIGINT:
        Globals.SCHED.remove_all_jobs()
        if Globals.SCHED.state == EVENT_SCHEDULER_START:
            Globals.SCHED.shutdown()
    exit(0)


def generate_graph() -> None:
    n_as = int(input("Por favor, ingrese la cantidad de AS's que desees: "))
    n_nodes = int(input("Ahora la cantidad de nodos que tendrá cada AS: "))

    ASs = []


def main() -> None:
    signal(SIGINT, signalHandler)

    as1 = AS(
        "as1",
        ["1a", "1b", "1c", "1d"],
        [
            ("1a", "1b", 8),
            ("1a", "1c", 15),
            ("1a", "1d", 5),
            ("1b", "1d", 5),
            ("1b", "1c", 1),
            ("1c", "1d", 9),
        ],
        ["1a", "1c"],
    )
    as2 = AS(
        "as2",
        ["2a", "2b", "2c", "2d"],
        [
            ("2a", "2b", 1),
            ("2a", "2c", 3),
            ("2a", "2d", 2),
            ("2b", "2d", 2),
            ("2b", "2c", 5),
            ("2c", "2d", 4),
        ],
        ["2a", "2c"],
    )
    as3 = AS(
        "as3",
        ["3a", "3b", "3c", "3d"],
        [
            ("3a", "3b", 9),
            ("3a", "3c", 2),
            ("3a", "3d", 4),
            ("3b", "3d", 5),
            ("3b", "3c", 6),
            ("3c", "3d", 7),
        ],
        ["3a"],
    )
    as4 = AS(
        "as4",
        ["4a", "4b", "4c", "4d"],
        [
            ("4a", "4a", 5),
            ("4a", "4c", 2),
            ("4a", "4d", 9),
            ("4b", "4d", 8),
            ("4b", "4c", 3),
            ("4c", "4d", 1),
        ],
        ["4a", "4c"],
    )
    as5 = AS(
        "as5",
        ["5a", "5b", "5c", "5d"],
        [
            ("5a", "5b", 7),
            ("5a", "5c", 5),
            ("5a", "5d", 1),
            ("5b", "5d", 3),
            ("5b", "5c", 1),
            ("5c", "5d", 9),
        ],
        ["5a", "5c"],
    )

    bgp1 = BGP(
        "bgp1",
        [as1, as2, as3, as4, as5],
        [
            ("4c", "1a", 20),
            ("4a", "5c", 60),
            ("1c", "2a", 30),
            ("2c", "3a", 10),
            ("3c", "5a", 15),
        ],
    )

    Globals.SCHED.start()
    Globals.DRAW_TIMER = 5

    while True:
        print_graph(bgp1, True)


@plotlive
def print_graph(graph: Graph, optimized: bool = False):
    graph.draw(optimized)


if __name__ == "__main__":
    main()
