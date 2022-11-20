from .node import Node
from .edge import Edge
from typing import Any, Sequence


class Graph(Node):
    def __init__(
        self,
        id: str,
        nodes: Sequence[Node | str],
        edges: Sequence[
            Edge
            | tuple[Node | str, Node | str, float, bool]
            | tuple[Node | str, Node | str, float]
        ] = [],
    ) -> None:
        super().__init__(id)
        parsed_nodes: list[Node] = [
            Node(node) if isinstance(node, str) else node for node in nodes
        ]
        self._nodes_id = set([node.id for node in parsed_nodes])
        assert len(self._nodes_id) == len(nodes), "Node IDs aren't unique"

        self._nodes = parsed_nodes
        self._edges: list[Edge] = []

        for edge in edges:
            if isinstance(edge, tuple):
                if len(edge) > 3:
                    edge = Edge(
                        node_a=Node(edge[0]) if isinstance(edge[0], str) else edge[0],
                        node_b=Node(edge[1]) if isinstance(edge[1], str) else edge[1],
                        weight=edge[2],
                        is_oriented=bool(edge[-1]),
                    )
                else:
                    edge = Edge(
                        node_a=Node(edge[0]) if isinstance(edge[0], str) else edge[0],
                        node_b=Node(edge[1]) if isinstance(edge[1], str) else edge[1],
                        weight=edge[2],
                    )
            self.add_edge(edge)

    @property
    def nodes(self) -> list[Node]:
        return self._nodes

    @property
    def nodes_id(self) -> set[str]:
        return self._nodes_id

    @property
    def edges(self) -> list[Edge]:
        return self._edges

    def __str__(self) -> str:
        text = "\nNodes: "
        for node in self._nodes:
            text += str(node) + " "

        text += "\nEdges: "
        for edge in self._edges:
            text += str(edge) + " "

        return text

    def add_node(self, node: Node) -> None:
        if not node.id in self._nodes_id:
            self._nodes.append(node)
            self._nodes_id.add(node.id)

    def add_edge(self, edge: Edge) -> None:
        self._validate_edge(edge)
        self._edges.append(edge)

    def _validate_edge(self, edge: Edge) -> None:
        assert (
            edge.node_a in self._nodes and edge.node_b in self._nodes
        ), f"Edge {str(edge)} isn't in the node list"

    def __new__(cls: type["Graph"], *args: Any, **kawgs: Any) -> "Graph":
        return object.__new__(cls)
