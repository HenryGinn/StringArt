import numpy as np

from utils import (
    get_values_indexes)


class Line():

    def __init__(self, art, start_index, end_index, color):
        self.art = art
        self.color = color
        self.set_pins(start_index, end_index)
        self.set_start_end_lookup()
        self.set_line_coefficients()
        self.name = f"{self.start_index:03}_{self.end_index:03}"

    def set_pins(self, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index
        self.start = self.art.pins[start_index]
        self.end = self.art.pins[end_index]

    def set_start_end_lookup(self):
        self.lookup = {
            self.start_index: self.end_index,
            self.end_index: self.start_index}

    def set_line_coefficients(self):
        self.x1, self.y1, self.x2, self.y2 = *self.start, *self.end
        self.a = self.y2 - self.y1
        self.b = self.x2 - self.x1
        self.c = self.x1*self.y2 - self.y1*self.x2

    def set_array(self):
        distance = self.get_distance()
        self.array = self.intensity_profile(distance)
        self.array = self.array[..., np.newaxis] * np.array(self.color)
        self.array = self.art.serialise(self.array)
        self.array = get_values_indexes(self.array)

    def get_distance(self):
        dot_x = self.a*self.art.x_coords
        dot_y = self.b*self.art.y_coords
        scale = np.sqrt(self.a**2 + self.b**2)
        distance = np.abs(dot_x - dot_y - self.c) / scale
        distance /= self.art.config.array_size
        distance = np.where(distance <= 1, distance, 1)
        return distance

    def intensity_profile(self, distance):
        linear_map = (self.art.intensity_gradient * distance
                      + self.art.intensity_intercept)
        intensity = np.maximum(np.minimum(1, linear_map), 0)
        return intensity

    def save(self):
        name = f"Line_{self.start_index}_{self.end_index}"
        array = get_grid(*self.array)
        self.art.save_array(self.array, name)

    def __str__(self):
        string = (
            f"Start index: {self.start_index}   End index: {self.end_index}")
        return string
