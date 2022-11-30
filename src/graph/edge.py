from .node import Node
from typing import Callable, Any
from enum import Enum
from copy import copy
from src.utils import Priority


class EdgeSubscriptionEnum(Enum):
    NODE_A = 0
    NODE_B = 1
    WEIGHT = 2
    IS_ORIENTED = 3


class Edge:
    def __init__(
        self,
        node_a: Node | str,
        node_b: Node | str,
        weight: float,
        is_oriented: bool = False,
        policy: Priority = Priority.LOW,
        subscriber: Callable[[EdgeSubscriptionEnum, "Edge"], Any] | None = None,
    ) -> None:
        if isinstance(node_a, str):
            node_a = Node(node_a)
        if isinstance(node_b, str):
            node_b = Node(node_b)

        self._node_a = node_a
        self._node_b = node_b
        self._weight = weight
        self._is_oriented = is_oriented
        self._policy = policy
        self._subscriber = subscriber

    @property
    def node_a(self) -> Node:
        return self._node_a

    @node_a.setter
    def node_a(self, new_value: Node) -> None:
        self._node_a = new_value
        if self._subscriber is not None:
            self._subscriber(EdgeSubscriptionEnum.NODE_A, self)

    @property
    def node_b(self) -> Node:
        return self._node_b

    @node_b.setter
    def node_b(self, new_value: Node) -> None:
        self._node_b = new_value
        if self._subscriber is not None:
            self._subscriber(EdgeSubscriptionEnum.NODE_B, self)

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, new_value: float) -> None:
        self._weight = round(new_value, 3)
        if self._subscriber is not None:
            self._subscriber(EdgeSubscriptionEnum.WEIGHT, self)

    @property
    def is_oriented(self) -> bool:
        return self._is_oriented

    @is_oriented.setter
    def is_oriented(self, new_value: bool) -> None:
        self._is_oriented = new_value
        if self._subscriber is not None:
            self._subscriber(EdgeSubscriptionEnum.IS_ORIENTED, self)

    @property
    def policy(self) -> Priority:
        return self._policy

    @property
    def subscriber(self) -> Callable[[EdgeSubscriptionEnum, "Edge"], Any] | None:
        return self._subscriber

    @subscriber.setter
    def subscriber(
        self, new_value: Callable[[EdgeSubscriptionEnum, "Edge"], Any] | None
    ):
        self._subscriber = new_value

    def __str__(self) -> str:
        text = f"({str(self.node_a.id)},{str(self.node_b.id)},{self.weight})"
        if not self.is_oriented:
            text += f" ({str(self.node_b.id)},{str(self.node_a.id)},{self.weight})"

        return text

    def copy(self) -> "Edge":
        return copy(self)

    def __hash__(self) -> int:
        return hash((self._node_a, self._node_b, self._weight, self._is_oriented))

    def __eq__(self, __o: "Edge") -> bool:
        if type(__o) is not self.__class__:
            return False

        return (
            self._node_a == __o.node_a
            and self._node_b == __o.node_b
            and self._weight == __o.weight
        )
