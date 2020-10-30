import math
import heapq
from dataclasses import dataclass, field
from enum import Enum, auto
from PIL import Image, ImageDraw, ImageOps, ImageChops
import numpy as np
from src.data import Node
from src.potential import MAX_POTENTIAL, MIN_POTENTIAL

from typing import List, Dict, Tuple, Optional, ClassVar


class NodeType(Enum):
    NEW = auto()
    OPEN = auto()
    CLOSE = auto()


@dataclass
class CalcNode:
    cnt: ClassVar[int] = 0
    cache: ClassVar[Dict[Tuple[int, int], 'CalcNode']] = {}

    @classmethod
    def new(cls, node):
        if node.as_tuple() not in cls.cache:
            cls.cache[node.as_tuple()] = CalcNode(node)
        return cls.cache[node.as_tuple()]

    node: Node
    id: int = 0
    fs: float = 0.0
    gs: float = 0.0
    nodetype: NodeType = NodeType.NEW
    parent: Optional['CalcNode'] = field(default=None, repr=False)
    _nexts: Optional[List['CalcNode']] = field(default=None, repr=False)

    def __post_init__(self, *args, **kwargs):
        self.id = CalcNode.cnt
        CalcNode.cnt += 1

    @property
    def x(self):
        return self.node.x

    @property
    def y(self):
        return self.node.y

    @property
    def nexts(self):
        if self._nexts is None:
            self._nexts = [CalcNode.new(edge.get_opposite_node(self.node)) for edge in self.node.edges]
        return self._nexts

    def __iter__(self):
        current = self
        while current is not None:
            yield current
            current = current.parent


class FastAstar:
    def __init__(self, start, goal, nodes, size, radius, strict=True):
        self.start = start
        self.goal = goal
        self.size = size
        self.radius = radius
        self.strict = strict
        self.overlap_cache = {}

        self.node_radius = {}
        if self.strict:
            for n in nodes:
                target = Image.new('L', self.size, color=MAX_POTENTIAL)
                draw = ImageDraw.Draw(target)
                draw.ellipse((n.x - self.radius, n.y - self.radius, n.x + self.radius, n.y + self.radius), fill=MIN_POTENTIAL)
                self.node_radius[(n.x, n.y)] = target.convert('1')

    def calculate(self, current_potential):
        target = None
        table = {}
        open_list = []
        CalcNode.cache = {}
        self.overlap_cache = {}

        heapq.heapify(open_list)

        start = CalcNode.new(self.start)
        start.fs = self._hs(start)

        table[start.id] = start
        heapq.heappush(open_list, (start.fs, start.id))

        while True:
            if len(open_list) == 0:
                print('No route found')
                return []

            target = table[heapq.heappop(open_list)[1]]
            if target.nodetype == NodeType.CLOSE:
                continue

            if target.node == self.goal:
                break

            target.nodetype = NodeType.CLOSE

            target.gs = target.fs - self._hs(target)

            for candidate in self._next(target, current_potential):
                fs = target.gs + self._cost(target, candidate) + self._hs(candidate)

                if candidate.nodetype == NodeType.NEW:
                    candidate.fs = fs
                    candidate.parent = target
                    candidate.nodetype = NodeType.OPEN
                    table[candidate.id] = candidate
                    heapq.heappush(open_list, (candidate.fs, candidate.id))
                else:
                    if fs < candidate.fs:
                        candidate.fs = fs
                        candidate.parent = target
                        candidate.nodetype = NodeType.OPEN
                        table[candidate.id] = candidate
                        heapq.heappush(open_list, (candidate.fs, candidate.id))

        path = [li.node for li in reversed(list(target))]

        return path

    def _check_overlap(self, x, y, current_potential):
        if (x, y) not in self.overlap_cache:
            potential = ImageOps.invert(Image.fromarray(current_potential))
            target = self.node_radius[(x, y)]
            img = ImageChops.logical_and(potential.convert('1'), target)
            self.overlap_cache[(x, y)] = np.any(np.array(img))
        return self.overlap_cache[(x, y)]

    def _next(self, target, current_potential):
        if self.strict:
            return [n for n in target.nexts if not self._check_overlap(n.x, n.y, current_potential)]
        else:
            return [n for n in target.nexts if not current_potential[n.y, n.x] == MAX_POTENTIAL]

    def _cost(self, target, candidate):
        return math.sqrt((candidate.x - target.x)**2 + (candidate.y - target.y)**2)

    def _hs(self, node):
        return math.sqrt((node.x - self.goal.x)**2 + (node.y - self.goal.y)**2)
