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
        self.o_x = float(const.COSTMAP_METADATA['origin']['point']['x'])
        self.o_y = float(const.COSTMAP_METADATA['origin']['point']['y'])
        self.resolution = float(const.COSTMAP_METADATA['resolution'])
        self.width = float(const.COSTMAP_METADATA['width'])
        self.height = float(const.COSTMAP_METADATA['height'])

    @property
    def initial(self):
        return np.array(Image.new('L', self.size, color=MIN_POTENTIAL))

    @property
    def current_field(self):
        if len(self.potentials.values()) == 0:
            return self.initial
        else:
            return np.minimum.reduce([v['field'] for v in self.potentials.values()])

    def register(self, id, path, radius):
        field = self._calc_potential(path, radius)
        self.potentials[id] = {
            'path': path,
            'field': field,
        }
        return self.potentials[id]

    def _calc_potential(self, path, potential_radius):
        img = Image.fromarray(self.initial)
        draw = ImageDraw.Draw(img)
        for node in path:
            xy = (node.x - potential_radius, node.y - potential_radius, node.x + potential_radius, node.y + potential_radius)
            draw.ellipse(xy, fill=MAX_POTENTIAL)
        draw.line([node.as_tuple() for node in path], fill=MAX_POTENTIAL, width=int(potential_radius * 2))
        return np.array(img)

    def _convert_pos(self, c_x, c_y):
        return int((c_x - self.o_x)/self.resolution), int(self.height - (c_y - self.o_y)/self.resolution)

    def _calc_point(self, c_x, c_y, potential_radius):
        x, y = self._convert_pos(c_x, c_y)
        img = Image.fromarray(self.initial)
        draw = ImageDraw.Draw(img)
        xy = (x - potential_radius, y - potential_radius, x + potential_radius, y + potential_radius)
        draw.ellipse(xy, fill=MAX_POTENTIAL)
        return np.array(img)

    def notify_pos(self, id, c_x, c_y, infration_radius):
        radius = infration_radius/self.resolution
        self.potentials[f'{id}_pos'] = {
            'field': self._calc_point(c_x, c_y, radius)
        }

        potential = self.potentials.get(id)
        if potential is None or potential.get('path') is None or len(potential['path']) == 0:
            return None

        target_wps = enumerate(potential['path'][:const.CHECK_WP_LENGTH], start=1)
        r = infration_radius * const.ERROR_MARGIN
        matched = next(filter(lambda wp: math.sqrt((wp[1].c_x - c_x) ** 2 + (wp[1].c_y - c_y) ** 2) < r, target_wps), None)
        if matched is None:
            return None

        passed = potential['path'][:matched[0]]
        path = potential['path'][matched[0]:]
        field = self._calc_potential(path, radius)
        self.potentials[id] = {
            'path': path,
            'field': field,
        }
        return passed

    def deregister(self, id):
        if id in self.potentials:
            del self.potentials[id]
