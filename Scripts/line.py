import numpy as np


class Line():

    def __init__(self, art, start_index, end_index):
        self.art = art
        self.set_pins(start_index, end_index)
        self.set_line_coefficients()

    def set_pins(self, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index
        self.start = self.art.pins[start_index]
        self.end = self.art.pins[end_index]

    def set_line_coefficients(self):
        self.x1, self.y1, self.x2, self.y2 = *self.start, *self.end
        self.a = self.y2 - self.y1
        self.b = self.x2 - self.x1
        self.c = self.x1*self.y2 - self.y1*self.x2

    def set_array(self):
        self.color = np.array([176, 11, 105])
        distance = self.get_distance()
        self.distance = distance
        self.array = self.intensity_profile(distance)
        self.array = 255 - ((1 - self.array[..., np.newaxis])
                            * (np.array([255, 255, 255]) - self.color))
        self.array = self.art.serialise(self.array)

    def get_distance(self):
        dot_x = self.a*self.art.x_coords
        dot_y = self.b*self.art.y_coords
        scale = np.sqrt(self.a**2 + self.b**2)
        distance = np.abs(dot_x - dot_y - self.c) / scale
        distance /= np.max(distance)
        return distance

    def intensity_profile(self, distance):
        width = 0.05
        intensity = np.where(distance < width, distance/width, 1)
        return intensity

    def save(self):
        name = f"Line_{self.start_index}_{self.end_index}"
        self.art.save_array(self.array, name)
