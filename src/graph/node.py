class Node(object):
    def __init__(self, id: str) -> None:
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    def __str__(self) -> str:
        return self._id

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __o: "Node") -> bool:
        if type(__o) != self.__class__:
            return False
        return self._id == __o._id
