from src.graph import Graph, DynamicGraph, Edge, EdgeSubscriptionEnum
from src.algorithm import bellman_ford
from .AS import AS


class BGP(DynamicGraph):
    def __init__(
        self,
        id: str,
        ASs: list[AS],
        edges: list[Edge | tuple[AS, AS, float, bool] | tuple[AS, AS, float]] = ...,
    ) -> None:
        super().__init__(id, ASs, edges)

        self._bellman_ford_per_AS: dict[str, tuple[Graph, dict[str, float]]] = {}
        self.__calc_bellman_ford_per_AS()

    def __str__(self) -> str:
        text = f"BGP '{self._id}'"

        text += "\n\nEDGES"
        for edge in self._edges:
            text += f" {str(edge)}"

        text += "\n\nAS's"
        for node in self._nodes:
            text += f"\n{str(node)}"

        text += "\n\nBELLMAN FORD"

        for [node_id, [_, distance]] in self._bellman_ford_per_AS.items():
            text += f"\n\nAS '{node_id}'"
            text += f"\nDISTANCE: {str(distance)}"

        return text

    def __calc_bellman_ford_per_AS(self) -> None:
        for AS in self._nodes:
            self._bellman_ford_per_AS[AS.id] = bellman_ford(self, AS)

    def _edge_subscription(self, type: EdgeSubscriptionEnum, edge: Edge) -> None:
        if type == EdgeSubscriptionEnum.WEIGHT:
            self.__calc_bellman_ford_per_AS()
        return super()._edge_subscription(type, edge)
