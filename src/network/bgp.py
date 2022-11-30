from src.graph import Graph, DynamicGraph, Edge, EdgeSubscriptionEnum, Node
from src.algorithm import bellman_ford
from typing import Sequence
from .AS import AS


class BGP(DynamicGraph):
    def __init__(
        self,
        id: str,
        ASs: list[AS],
        edges: Sequence[
            Edge
            | tuple[Node | str, Node | str, float, bool]
            | tuple[Node | str, Node | str, float]
        ] = ...,
    ) -> None:
        super().__init__(id, ASs, edges)

        bellman_ford_nodes: set[Node] = set()
        for edge in self._edges:
            bellman_ford_nodes.add(edge.node_a)
            bellman_ford_nodes.add(edge.node_b)
        self._bellman_ford_nodes = list(bellman_ford_nodes)

        self._single_graph = Graph(id + ".bellman-ford", ASs)

        self._bellman_ford_per_AS: dict[str, tuple[Graph, dict[str, float]]] = {}
        self.__calc_bellman_ford_per_AS()

    def _validate_edge(self, edge: Edge) -> None:
        pass

    def __str__(self) -> str:
        text = f"BGP '{self._id}'"

        text += "\n\nNODES"
        for node in self._nodes:
            text += f" {node.id}"

        text += "\n\nEDGES"
        for edge in self._edges:
            text += f" {str(edge)}"

        text += "\n\nAS's"
        for node in self._nodes:
            text += f"\n{str(node)}"

        text += "\n\nBELLMAN FORD"

        for [node_id, [graph, distance]] in self._bellman_ford_per_AS.items():
            text += f"\n\nAS '{node_id}'"
            text += "\nEDGES: "
            for edge in graph.edges:
                text += f"{str(edge)} "
            text += f"\nDISTANCE: {str(distance)}"

        return text

    def draw(self, optimized: bool = False) -> None:
        graph = Graph(self.id + "_print", [])
        for child_graph in self.nodes:
            child_graph: AS
            for node in child_graph.nodes:
                graph.add_node(node)

            if optimized:
                [dijkstra_graph, _] = list(child_graph.dijkstra_per_gateway.values())[0]
                for edge in dijkstra_graph.edges:
                    graph.add_edge(edge)
            else:
                for edge in child_graph.edges:
                    graph.add_edge(edge)

        if optimized:
            for [bellman_ford_graph, _] in self._bellman_ford_per_AS.values():
                for edge in bellman_ford_graph.edges:
                    graph.add_edge(edge)

        else:
            for edge in self._edges:
                graph.add_edge(edge)

        graph.draw(optimized)

    def __calc_bellman_ford_per_AS(self) -> None:
        for node in self._bellman_ford_nodes:
            self._bellman_ford_per_AS[node.id] = bellman_ford(
                Graph(self.id, self._bellman_ford_nodes, self._edges), node
            )

    def _edge_subscription(self, type: EdgeSubscriptionEnum, edge: Edge) -> None:
        if type == EdgeSubscriptionEnum.WEIGHT:
            self.__calc_bellman_ford_per_AS()
        return super()._edge_subscription(type, edge)
