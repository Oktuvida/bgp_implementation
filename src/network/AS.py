from src.graph import Node, DynamicGraph, Graph, EdgeSubscriptionEnum, Edge
from src.algorithm import dijkstra


class AS(DynamicGraph):
    def __init__(
        self,
        id: str,
        nodes: list[Node | str],
        gateway_nodes: list[Node | str],
        edges: list[
            Edge
            | tuple[Node | str, Node | str, float, bool]
            | tuple[Node | str, Node | str, float]
        ] = [],
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

    def __edge_subscription(self, type: EdgeSubscriptionEnum, edge: Edge) -> None:
        if type == EdgeSubscriptionEnum.WEIGHT:
            self.__calc_dijkstra_per_gateway()

    def add_edge(self, edge: Edge) -> None:
        edge.subscriber = self.__edge_subscription
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
