from src.graph import Node, DynamicGraph, Graph, EdgeSubscriptionEnum, Edge
from src.algorithm import dijkstra
from typing import Sequence, Self
import networkx as nx
import matplotlib.pyplot as plt


class AS(DynamicGraph):
    def __init__(
        self,
        id: str,
        nodes: Sequence[Node | str | Graph],
        edges: Sequence[
            Edge
            | tuple[Node | str, Node | str, float, bool]
            | tuple[Node | str, Node | str, float]
        ] = [],
        gateway_nodes: Sequence[Node | str] = [],
    ) -> None:
        super().__init__(id, nodes, edges)
        parsed_gateway_nodes: list[Node] = [
            Node(node) if isinstance(node, str) else node for node in gateway_nodes
        ]
        self._gateway_nodes: list[Node] = []
        self._dijkstra_per_gateway: dict[str, tuple[Graph, dict[str, float]]] = {}
        for node in parsed_gateway_nodes:
            assert node in self._nodes, "Gateway node isn't in nodes declaration"
            self._gateway_nodes.append(node)

        self.__calc_dijkstra_per_gateway()

    @property
    def gateway_nodes(self) -> list[Node]:
        return self._gateway_nodes

    @property
    def dijkstra_per_gateway(self) -> dict[str, tuple[Graph, dict[str, float]]]:
        return self._dijkstra_per_gateway

    def draw(self, optimized: bool = False) -> None:
        if not optimized:
            return super().draw(optimized)

        grid_size = len(self._dijkstra_per_gateway.keys())
        plot_counter = 1
        for [graph, _] in self._dijkstra_per_gateway.values():
            plt.subplot(grid_size, grid_size // 2, plot_counter)
            plot_counter += 1
            graph.draw(optimized)

    def _edge_subscription(self, type: EdgeSubscriptionEnum, edge: Edge) -> None:
        if type == EdgeSubscriptionEnum.WEIGHT:
            self.__calc_dijkstra_per_gateway()

    def add_edge(self, edge: Edge) -> None:
        edge.subscriber = self._edge_subscription
        return super().add_edge(edge)

    def __calc_dijkstra_per_gateway(self) -> None:
        for node in self._gateway_nodes:
            self._dijkstra_per_gateway[node.id] = dijkstra(self, node)

    def __str__(self) -> str:
        text = f"\nAS '{self._id}'"
        text += super().__str__()

        text += "\n\nDijkstra's gateways:"
        for [node, [dijkstra, distance]] in self._dijkstra_per_gateway.items():
            text += f"\n\nGATEWAY '{str(node)}'"
            text += f"\n{str(dijkstra)}"
            text += f"\nDISTANCE: {str(distance)}"

        return text
