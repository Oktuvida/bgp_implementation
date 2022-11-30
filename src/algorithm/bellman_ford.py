from src.graph import Graph, Node, Edge
from sys import maxsize as MAXSIZE
from time import time


def bellman_ford(src_graph: Graph, start_node: Node) -> tuple[Graph, dict[str, float]]:
    parsed_start_node = Node(start_node) if isinstance(start_node, str) else start_node
    assert parsed_start_node in src_graph.nodes, f"Start node isn't in the node list"

    distance: dict[str, float] = {}
    distance[parsed_start_node.id] = 0

    dst_graph = Graph(f"{src_graph.id}.{time()}", [start_node], [])
    for _ in range(len(src_graph.nodes) - 1):
        for edge in src_graph.edges:
            distance_node_a = distance.get(edge.node_a.id, MAXSIZE)
            distance_node_b = distance.get(edge.node_b.id, MAXSIZE)
            edge_involved = edge.copy()
            edge_involved.is_oriented = True
            edge_weight = edge_involved.weight * edge_involved.policy

            if distance_node_b > distance_node_a + edge_weight:
                distance[edge.node_b.id] = distance_node_a + edge_weight

                dst_graph.add_node(edge.node_a)
                dst_graph.add_node(edge.node_b)

                dst_graph.add_edge(edge_involved)
            elif (
                not edge.is_oriented and distance_node_a > distance_node_b + edge_weight
            ):
                distance[edge.node_a.id] = distance_node_b + edge_weight

                dst_graph.add_node(edge.node_a)
                dst_graph.add_node(edge.node_b)

                edge_involved.node_a = edge.node_b
                edge_involved.node_b = edge.node_a
                dst_graph.add_edge(edge_involved)

    return (dst_graph, distance)
