import os
import sys

import numpy as np
from PIL import Image

from config import Config
from line import Line
from least_squares import LeastSquares
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
        self.least_squares = LeastSquares(self)

    def ensure_configured(self):
        if not self.configured:
            self.configure(force=False)

    def configure(self, force=True):
        self.config.configure(force)

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


    # Loading/computing lines

    def initialise_lines(self):
        self.lines = [
            Line(self, pin_1_index, pin_2_index)
            for pin_1_index in range(self.config.pin_count)
            for pin_2_index in range(self.config.pin_count)
            if pin_1_index < pin_2_index]

    def set_lines(self):
        self.ensure_lines_initialised()
        if self.lines_files_exists():
            self.set_lines_from_file()
        else:
            self.set_lines_from_new()

    def ensure_lines_initialised(self):
        self.ensure_configured()
        if not hasattr(self, "lines"):
            self.initialise_lines()

    def lines_files_exists(self):
        self.set_lines_paths()
        return os.path.exists(self.lines_path)

    def set_lines_paths(self):
        lines_file_name = (
            f"Name_{self.name}__"
            f"Size_{self.config.array_size}__"
            f"PinCount_{self.config.pin_count}.npy")
        self.lines_path = os.path.join(self.folder_path, lines_file_name)

    def set_lines_from_file(self):
        print("Loading line data")
        line_arrays = np.load(self.lines_path, allow_pickle=False)
        for line, array in zip(self.lines, line_arrays):
            line.array = array

    def set_lines_from_new(self):
        print("Generating line data")
        self.set_meshgrid()
        self.generate_line_arrays()
        self.save_lines()

    def generate_line_arrays(self):
        for line in self.lines:
            line.set_array()

    def save_lines(self):
        line_arrays = np.stack([line.array for line in self.lines])
        np.save(self.lines_path, line_arrays, allow_pickle=False)



    # Utils

    def serialise(self, array):
        serial = array[*self.circle_indexes, :]
        return serial

    def unserialise(self, serial):
        array = self.blank_array.copy()
        array[*self.circle_indexes, :] = serial
        return array

    def ensure_unserialised(self, array):
        if array.ndim > 2:
            return array
        else:
            return self.unserialise(array)

    def save_array(self, array, name):
        print(array.shape)
        array = self.ensure_unserialised(array)
        print(array.shape)
        image = get_image_from_array(array)
        new_size = int(np.ceil(1000 / image.size[0]) * image.size[0])
        image = image.resize((new_size, new_size), resample=Image.BOX)
        path = os.path.join(self.folder_path, f"{name}.png")
        image.save(path)

    def get_path_string(self):
        path_string = (
            f"Repository path: {self.repository_path}\n"
            f"Folder path: {self.folder_path}\n"
            f"Source image path: {self.source_path}\n")
        return path_string

    def __str__(self):
        string = f"{self.get_path_string()}"
        return string





















