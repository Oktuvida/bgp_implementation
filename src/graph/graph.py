from .node import Node
from .edge import Edge
from typing import Any, Sequence, Self
import networkx as nx


class Graph(Node, object):
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

    def to_networkx(self, oriented: bool = False) -> Any:
        if oriented:
            nx_graph = nx.DiGraph()
        else:
            nx_graph = nx.Graph()

        for edge in self._edges:
            nx_graph.add_edge(edge.node_a.id, edge.node_b.id, weight=edge.weight)

        return nx_graph

    def draw(self, optimized: bool = False) -> None:
        nx_graph = self.to_networkx(oriented=optimized)

        fixed_pos: dict[str, tuple[float, float]] = {}

        x_coord = 0
        for node, index in zip(self._nodes, range(len(self._nodes))):
            if index % 2 == 0:
                fixed_pos[node.id] = (x_coord, 1)
            else:
                fixed_pos[node.id] = (x_coord, 2)
                x_coord += 1

        pos = nx.spring_layout(nx_graph, pos=fixed_pos, fixed=fixed_pos.keys())
        # pos = nx.spring_layout(nx_graph)
        nx.draw_networkx(nx_graph, pos, node_size=600, with_labels=True)

        edge_labels = nx.get_edge_attributes(nx_graph, "weight")
        nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels)

    def _validate_edge(self, edge: Edge) -> None:
        assert (
            edge.node_a in self._nodes and edge.node_b in self._nodes
        ), f"Edge {str(edge)} isn't in the node list"
