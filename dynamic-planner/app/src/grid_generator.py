import json
import re

import numpy as np

from src.data import Vertex


class Grid:
    def __init__(self, map_pgm, metadata_json, u_length_m=0.8):
        self.image = map_pgm
        self.resolution, self.origin_mm = self.process_metadata(metadata_json)
        self.unit_length = int(u_length_m / self.resolution)
        self.raw_image, self.cost_map, self.origin_px = self.process_image()
        self.size

    def process_metadata(self, metadata_json):
        metadata = json.loads(metadata_json.read())
        origin = tuple([float(o) for o in metadata['origin'][0:2]])
        return float(metadata['resolution']), origin

    def process_image(self):
        raw_image = np.array(self.read_pgm())
        raw_image[raw_image < 210] = 0
        raw_image[raw_image > 210] = 255
        raw_image = np.rot90(np.flip(raw_image, 0), 3)
        size = raw_image.shape

        self.h_units = int(size[0] / self.unit_length)
        self.v_units = int(size[1] / self.unit_length)

        return raw_image, np.zeros([self.h_units, self.v_units]), self.get_origin_px(size)

    def get_origin_px(self, image_size):
        origin_x = int(-self.origin_mm[0] / self.resolution)
        origin_y = int(image_size[1] + (self.origin_mm[1] / self.resolution))
        return (origin_x, origin_y)

    def set_obstacles(self):
        width, height = self.cost_map.shape
        num_pixls = self.unit_length ** 2

        for i in range(self.h_units):
            for j in range(self.v_units):
                x0, x1 = int(i * self.unit_length + 1), int((i + 1) * self.unit_length)
                y0, y1 = int(j * self.unit_length + 1), int((j + 1) * self.unit_length)
                non_zeros = np.count_nonzero(self.raw_image[x0:x1, y0:y1])
                if (non_zeros / num_pixls) < 0.85:
                    self.cost_map[i, j] = 100

    def build_graph(self):
        self.set_obstacles()
        free_cells = np.argwhere(np.array(self.cost_map) == 0)
        neighbors = np.array([[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]])

        graph = dict()

        for cell in free_cells:
            current_vertex = self.get_center(cell)
            converted_current_vertex = self.convert_coordinates(current_vertex)
            vertex = Vertex(current_vertex, converted_current_vertex)

            graph[vertex] = list()
            for neighbor in neighbors:
                neighbor_coord = cell + neighbor
                if self.cost_map[neighbor_coord[0]][neighbor_coord[1]] == 0:
                    p_vertex = self.get_center(neighbor_coord)
                    c_vertex = self.convert_coordinates(p_vertex)
                    graph[vertex].append(Vertex(p_vertex, c_vertex))

        return graph

    def get_center(self, cell: np.ndarray):
        return int(cell[0] * self.unit_length + self.unit_length / 2), int(cell[1] * self.unit_length + self.unit_length / 2)

    def convert_coordinates(self, screen_coordinate):
        x = round(float((screen_coordinate[0] - self.origin_px[0]) * self.resolution), 3)
        y = round(float((-screen_coordinate[1] + self.origin_px[1]) * self.resolution), 3)
        return (x, y)

    def read_pgm(self, byte_order: str = '>'):
        buffer = self.image.read()
        match_bytes = re.search(
            b"(^P5\\s(?:\\s*#.*[\r\n])*"
            b"(\\d+)\\s(?:\\s*#.*[\r\n])*"
            b"(\\d+)\\s(?:\\s*#.*[\r\n])*"
            b"(\\d+)\\s(?:\\s*#.*[\r\n]\\s)*)", buffer)
        if match_bytes:
            header, width, height, maxval = match_bytes.groups()
            self.size = (int(width), int(height))
        else:
            raise ValueError(f"Not a raw PGM file: '{self.image.filename}'")
        return np.frombuffer(buffer,
                             dtype='u1' if int(maxval) < 256 else byte_order + 'u2',
                             count=int(width) * int(height),
                             offset=len(header)
                             ).reshape((int(height), int(width)))
