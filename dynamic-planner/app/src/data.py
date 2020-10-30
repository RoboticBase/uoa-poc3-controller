from dataclasses import dataclass, field

from typing import List, Tuple, Optional


@dataclass(order=True, frozen=True)
class Vertex:
    pixel: Tuple[int, int]
    converted: Tuple[float, float]


@dataclass
class Node:
    x: int
    y: int
    c_x: Optional[float] = None
    c_y: Optional[float] = None
    edges: List['Edge'] = field(default_factory=list, repr=False)

    def as_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


@dataclass
class Edge:
    st: Node
    ed: Node

    def get_opposite_node(self, node: Node) -> Node:
        return self.ed if self.st == node else self.st
