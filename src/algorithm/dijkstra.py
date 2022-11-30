from src.graph import Graph, Node, Edge
from sys import maxsize as MAXSIZE
from time import time


def update_min_distance(
    src_graph: Graph, dst_graph: Graph, distance: dict[str, float]
) -> None:
    node_involved: Node | None = None
    edge_involved: Edge | None = None
    min_distance = MAXSIZE

    for node in dst_graph.nodes:
        current_distance = distance.get(node.id, MAXSIZE)
        for edge in src_graph.edges:
            if min_distance > (edge.weight + current_distance):
                if edge.node_a == node and edge.node_b.id not in dst_graph.nodes_id:
                    node_involved = edge.node_b
                    edge_involved = edge.copy()
                    min_distance = edge.weight + current_distance
                if (
                    not edge.is_oriented
                    and edge.node_b == node
                    and edge.node_a.id not in dst_graph.nodes_id
                ):
                    node_involved = edge.node_a
                    edge_involved = edge.copy()
                    edge_involved.node_a = edge.node_b
                    edge_involved.node_b = edge.node_a
                    min_distance = edge.weight + current_distance

    if node_involved is not None and edge_involved is not None:
        edge_involved.is_oriented = True
        dst_graph.add_node(node_involved)
        dst_graph.add_edge(edge_involved)
        distance[node_involved.id] = min_distance


def dijkstra(
    src_graph: Graph, start_node: Node | str
) -> tuple[Graph, dict[str, float]]:
    parsed_start_node: Node = (
        Node(start_node) if isinstance(start_node, str) else start_node
    )
    assert parsed_start_node in src_graph.nodes, "Start node isn't in the node list"

    distance: dict[str, float] = {}
    distance[parsed_start_node.id] = 0

    dst_graph = Graph(f"{src_graph.id}.{time()}", [start_node], [])
    for _ in range(len(src_graph.nodes) - 1):
        update_min_distance(src_graph, dst_graph, distance)

    return (dst_graph, distance)
