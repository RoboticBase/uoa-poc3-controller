from dataclasses import dataclass, field
from enum import Enum, auto

from src import const

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

    def as_tuple(self):
        return (self.x, self.y)


@dataclass
class Edge:
    st: Node
    ed: Node

    def get_opposite_node(self, node):
        return self.ed if self.st == node else self.st


class ReqState(Enum):
    NEW = auto()
    RETRY = auto()


@dataclass
class Req:
    robot_id: str
    start_node: str
    dest_node: str
    dest_angle: str
    inflation_radius: float
    state: ReqState = ReqState.NEW


class Mode(Enum):
    NAVI = const.MODE_NAVI
    STANDBY = const.MODE_STAQNDBY
    ERROR = const.MODE_ERROR
    UNKNOWN = const.MODE_UNKNOWN

    @classmethod
    def value_of(cls, s):
        return next(filter(lambda e: e.value == s, Mode), Mode.UNKNOWN)


@dataclass
class State:
    current_mode: Mode = Mode.UNKNOWN
    next_mode: Mode = Mode.UNKNOWN
    update_count: int = 0

    def update(self, modeStr):
        mode = Mode.value_of(modeStr)
        if self.next_mode != mode:
            self.next_mode = mode
            self.update_count = 1
        else:
            if self.current_mode != self.next_mode:
                self.update_count += 1
                if self.update_count >= const.MODE_CHANGE_COUNT:
                    self.current_mode = mode
                    self.next_mode = mode
                    return True
        return False
