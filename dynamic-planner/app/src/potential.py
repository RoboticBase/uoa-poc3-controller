import math
from PIL import Image, ImageDraw
import numpy as np

MAX_POTENTIAL = 0
MIN_POTENTIAL = 255


class Potential:
    def __init__(self, size, error_margin):
        self.size = size
        self.error_margin = error_margin
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

    def register(self, id, path, potential_radius):
        field = self._calc_potential(path, potential_radius, self.initial)
        self.potentials[id] = {'path': path, 'field': field, 'radius': potential_radius}
        return self.potentials[id]

    def _calc_potential(self, path, potential_radius, potentials):
        img = Image.fromarray(potentials)
        draw = ImageDraw.Draw(img)
        for node in path:
            xy = (node.x - potential_radius, node.y - potential_radius, node.x + potential_radius, node.y + potential_radius)
            draw.ellipse(xy, fill=MAX_POTENTIAL)
        draw.line([node.as_tuple() for node in path], fill=MAX_POTENTIAL, width=int(potential_radius * 2))
        return np.array(img)

    def notify_pos(self, id, x, y):
        potential = self.potentials.get(id)
        if potential is None or potential.get('path') is None or len(potential['path']) == 0:
            return False
        top_wp = potential['path'][0]
        if math.sqrt((top_wp.x - x)**2 + (top_wp.y - y)**2) < potential['radius'] * self.error_margin:
            path = [] if len(potential['path']) == 1 else potential['path'][1:]
            field = self._calc_potential(path, potential['radius'], self.initial)
            self.potentials[id] = {'path': path, 'field': field, 'radius': potential['radius']}
            return True
        return False
