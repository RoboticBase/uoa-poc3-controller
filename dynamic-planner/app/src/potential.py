import math
from PIL import Image, ImageDraw
import numpy as np

from src import const

MAX_POTENTIAL = 0
MIN_POTENTIAL = 255


class Potential:
    def __init__(self, size):
        self.size = size
        self.potentials = {}

    @property
    def initial(self):
        return np.array(Image.new('L', self.size, color=MIN_POTENTIAL))

    @property
    def current_field(self):
        if len(self.potentials.values()) == 0:
            return self.initial
        else:
            return np.minimum.reduce([v['field'] for v in self.potentials.values()])

    def register(self, id, path, radius, infration_radius):
        field = self._calc_potential(path, radius, self.initial)
        self.potentials[id] = {
            'path': path,
            'field': field,
            'radius': radius,
            'infration_radius': infration_radius
        }
        return self.potentials[id]

    def _calc_potential(self, path, potential_radius, potentials):
        img = Image.fromarray(potentials)
        draw = ImageDraw.Draw(img)
        for node in path:
            xy = (node.x - potential_radius, node.y - potential_radius, node.x + potential_radius, node.y + potential_radius)
            draw.ellipse(xy, fill=MAX_POTENTIAL)
        draw.line([node.as_tuple() for node in path], fill=MAX_POTENTIAL, width=int(potential_radius * 2))
        return np.array(img)

    def notify_pos(self, id, c_x, c_y):
        potential = self.potentials.get(id)
        if potential is None or potential.get('path') is None or len(potential['path']) == 0:
            return None

        target_wps = enumerate(potential['path'][:const.CHECK_WP_LENGTH], start=1)
        r = potential['infration_radius'] * const.ERROR_MARGIN
        matched = next(filter(lambda wp: math.sqrt((wp[1].c_x - c_x) ** 2 + (wp[1].c_y - c_y) ** 2) < r, target_wps), None)
        if matched is None:
            return None

        passed = potential['path'][:matched[0]]
        path = potential['path'][matched[0]:]
        field = self._calc_potential(path, potential['radius'], self.initial)
        self.potentials[id] = {
            'path': path,
            'field': field,
            'radius': potential['radius'],
            'infration_radius': potential['infration_radius']
        }
        return passed
