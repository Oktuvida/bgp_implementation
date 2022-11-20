from .graph import Graph
from .edge import Edge, EdgeSubscriptionEnum
from .node import Node
from typing import Sequence
from random import random, choice, randint
from src.utils import Globals


class DynamicGraph(Graph):
    def __init__(
        self,
        id: str,
        nodes: Sequence[Node | str],
        edges: Sequence[
            Edge
            | tuple[Node | str, Node | str, float, bool]
            | tuple[Node | str, Node | str, float]
        ] = ...,
    ) -> None:
        super().__init__(id, nodes, edges)
        Globals.SCHED.add_job(self._update_weights, "interval", seconds=randint(5, 10))
        for edge in self._edges:
            edge.subscriber = self._edge_subscription

    def _update_weights(self) -> None:
        for edge in self._edges:
            edge.weight += choice([-1, 1]) * random() * edge.weight * 0.2

    def _edge_subscription(self, type: EdgeSubscriptionEnum, edge: Edge) -> None:
        pass
