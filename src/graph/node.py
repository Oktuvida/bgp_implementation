node_instances: dict[str, "Node"] = {}


class Node(object):
    def __init__(self, id: str) -> None:
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    def __str__(self) -> str:
        return self._id

    def __new__(cls: type["Node"], id: str) -> "Node":
        if node_instances.get(id) is None:
            node_instances[id] = super().__new__(cls)
        return node_instances[id]
