from math import floor, ceil

import numpy as np


class Line():

    def __init__(self, art, pin_start_index, pin_end_index):
        self.art = art
        self.set_pins(pin_start_index, pin_end_index)
        self.set_line_coefficients()
        self.color = np.array([176, 11, 105])

    def set_pins(self, pin_start_index, pin_end_index):
        self.pin_start_index = pin_start_index
        self.pin_end_index = pin_end_index
        self.pin_start = self.art.pins[pin_start_index]
        self.pin_end = self.art.pins[pin_end_index]

    def set_line_coefficients(self):
        self.x1, self.y1, self.x2, self.y2 = *self.pin_start, *self.pin_end
        self.a = self.y2 - self.y1
        self.b = self.x2 - self.x1
        self.c = self.x1*self.y2 - self.y1*self.x2

    def set_array(self):
        distance = self.get_distance()
        self.distance = distance
        self.array = self.intensity_profile(distance)
        self.array = 255 - (1-self.array[..., np.newaxis])*(np.array([255, 255, 255]) - self.color)

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
        self.art.save_array(self.array, f"Line_{self.pin_end_index}")

def fpart(x):
    return x - ipart(x)

def ipart(x):
    return floor(x)
