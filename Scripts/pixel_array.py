import os

import numpy as np
import matplotlib.colors as mcol
from hgutilities import defaults
from PIL import Image

from utils import resize_figure


class PixelArray():

    def __init__(self, art):
        self.art = art
        self.inherit_from_setup_position()
        self.art_size = int(2 * self.pin_radius)

    def inherit_from_setup_position(self):
        kwargs = ["figure", "pin_radius",
                  "x_position", "y_position",
                  "image_width", "image_height",
                  "background_color"]
        defaults.inherit(self, self.art.setup_position_obj, kwargs)

    def set_array(self):
        self.set_figure()
        self.set_array_shape()
        self.initialise_array()
        self.display_image()

    def set_figure(self):
        self.figure = self.figure.convert(mode="RGB")
        self.figure = self.figure.reduce(10)
        self.figure = np.array(self.figure)

    # The array needs to conform to the figure size and also have
    # the circle of pins be the right size relative to the figure.
    def set_array_shape(self):
        self.figure_size = max(self.figure.shape[:2])
        max_image_dimension = max(self.image_width, self.image_height)
        pin_image_ratio = 2*self.pin_radius/max_image_dimension
        self.array_size = int(np.ceil(pin_image_ratio * self.figure_size))
        self.array_shape = (self.array_size, self.array_size, 3)

    def initialise_array(self):
        self.set_circle_array()
        background_color_array = self.get_color_array(self.background_color)
        surroundings_array = self.get_color_array("#021b34")
        self.array = np.where(
            self.circle_array, background_color_array, surroundings_array)

    def set_circle_array(self):
        circle_array = self.get_circle_array_two_dimensions()
        circle_array = np.stack((circle_array, circle_array, circle_array))
        self.circle_array = np.moveaxis(circle_array, 0, 2)

    def get_circle_array_two_dimensions(self):
        radius = (self.array_size - 1) // 2
        constructer = self.get_circle_constructer_array(radius)
        x, y = np.meshgrid(constructer, constructer)
        pixel_distance = np.sqrt(x**2 + y**2)
        circle = np.where(pixel_distance <= radius+0.1, 1, 0)
        return circle

    def get_circle_constructer_array(self, radius):
        left = np.linspace(radius, 0, radius+1)
        right = self.get_circle_constructure_array_right(radius)
        circle_constructer = np.concatenate((left, right))
        return circle_constructer

    def get_circle_constructure_array_right(self, radius):
        if self.array_size % 2 == 1:
            return np.linspace(1, radius, radius)
        else:
            return np.linspace(0, radius, radius + 1)

    def get_color_array(self, color):
        color_array = np.array(mcol.to_rgb(color)) * 255
        color_array = np.ones(self.array_shape)*color_array
        return color_array

    def print_help(self, obj):
        for i in dir(obj):
            if i != "__array_interface__":
                print(i, getattr(obj, i))
                help(getattr(obj, i))
                print("")


    def display_image(self):
        self.convert_array_to_image()
        PIL_figure = resize_figure(self.image, self.art_size, self.art_size)
        path = os.path.join(self.art.folder_path, "Output.png")
        PIL_figure.save(path)
    
    def convert_array_to_image(self):
        array = np.where(np.isnan(self.array), 0, self.array)
        self.image = Image.fromarray(np.uint8(array))

    
        



























