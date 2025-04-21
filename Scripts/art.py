import os
import sys

import numpy as np
from PIL import Image

from config import Config
from pixel_array import PixelArray
from line import Line
from utils import get_image_from_array

class Art():

    def __init__(self, folder_name, source_name):
        self.process_path_data(folder_name, source_name)
        self.set_objects()
        self.configured = False

    def process_path_data(self, folder_name, source_name):
        self.name = folder_name
        self.repository_path = os.path.split(sys.path[0])[0]
        self.folder_path = os.path.join(self.repository_path, "Data", folder_name)
        self.source_path = os.path.join(self.folder_path, source_name)

    def set_objects(self):
        self.config = Config(self)

    def ensure_configured(self):
        if not self.configured:
            self.configure(force=False)

    def configure(self, force=True):
        self.config.configure(force)
        self.source_array = self.config.source_array
        self.set_meshgrid()
        self.set_lines()

    def set_meshgrid(self):
        coords = np.arange(self.config.array_size)
        self.x_coords, self.y_coords = np.meshgrid(coords, coords)
        # These are to shift things to the coordinates of the centre of
        # the cells instead of the corners. I do not understand why
        # these offsets are not 0.5. Visually, 0.25 gives better results
        # when comparing a low resolution grid to a high resolution
        # grid. Given that in practice a high resolution grid will
        # always be used and the difference scales with the cell size,
        # this does not matter anyway.
        self.x_coords = self.x_coords - 0.25
        self.y_coords = self.y_coords - 0.25

    def set_pixel_array(self):
        self.ensure_configured()
        self.pixel_array_obj = PixelArray(self)
        self.pixel_array_obj.set_array()

    def get_path_string(self):
        path_string = (f"Repository path: {self.repository_path}\n"
                       f"Folder path: {self.folder_path}\n"
                       f"Source image path: {self.source_path}\n")
        return path_string

    def save_array(self, array, name):
        image = get_image_from_array(array)
        new_size = int(np.ceil(1000 / image.size[0]) * image.size[0])
        image = image.resize((new_size, new_size), resample=Image.BOX)
        path = os.path.join(self.folder_path, f"{name}.png")
        image.save(path)


    # Computing lines

    def set_lines(self):
        self.lines = [
            Line(self, pin_1_index, pin_2_index)
            for pin_1_index in range(self.config.pin_count)[:1]
            for pin_2_index in range(self.config.pin_count)[3:4]]

    def compute_lines(self):
        for line in self.lines[:1]:
            line.set_array()
            line.save()

    def __str__(self):
        string = f"{self.get_path_string()}"
        return string





















