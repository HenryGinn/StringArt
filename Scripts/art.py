import os
import sys

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from config import Config
from line import Line
from least_squares import LeastSquares
from greedy import Greedy
from utils import (
    get_image_from_array,
    pack,
    unpack)


grayscale_map = np.array([0.299, 0.587, 0.114])


class Art():

    def __init__(self, folder_name, source_name):
        self.process_path_data(folder_name, source_name)
        self.config = Config(self)
        self.configured = False

    def process_path_data(self, folder_name, source_name):
        self.name = folder_name
        self.repository_path = os.path.split(sys.path[0])[0]
        self.folder_path = os.path.join(self.repository_path, "Data", folder_name)
        self.source_path = os.path.join(self.folder_path, source_name)

    def set_physical_parameters(self, thread_width=0.002, diameter=0.6):
        self.thread_width = thread_width
        self.diameter = diameter
        self.thread_diameter_ratio = thread_width / diameter
        self.set_intensity_profile_parameters()

    def set_intensity_profile_parameters(self):
        inner_width = self.thread_diameter_ratio * 0.7
        outer_width = inner_width * 2
        self.intensity_gradient = 2 / (inner_width - outer_width)
        self.intensity_intercept = -self.intensity_gradient * outer_width / 2

    def initialise_least_squares(self):
        self.ensure_lines_setup()
        self.least_squares = LeastSquares(self)
        return self.least_squares

    def initialise_greedy(self):
        self.ensure_lines_setup()
        self.greedy = Greedy(self)
        return self.greedy

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

    def convert_to_grayscale(self):
        self.array = grayscale_map * self.array


    # Loading/computing lines

    def setup_lines(self, force=False):
        self.ensure_configured()
        self.initialise_lines()
        self.set_line_lookup()
        self.set_line_paths()
        self.set_line_arrays(force)

    def initialise_lines(self):
        self.lines = [
            Line(self, pin_1_index, pin_2_index)
            for pin_1_index in range(self.config.pin_count)
            for pin_2_index in range(self.config.pin_count)
            if pin_1_index < pin_2_index][29:30]

    def set_line_lookup(self):
        self.line_lookup = {
            pin_index: [
                line for line in self.lines
                if (line.start_index == pin_index or
                    line.end_index == pin_index)]
            for pin_index in range(self.config.pin_count)}

    def set_line_arrays(self, force=False):
        if force or not self.line_paths_exist():
            self.set_lines_from_new()
        else:
            self.set_lines_from_file()

    def line_paths_exist(self):
        return (
            os.path.exists(self.line_data_path) and
            os.path.exists(self.line_sizes_path))
    
    def ensure_lines_setup(self):
        self.ensure_configured()
        if not hasattr(self, "lines"):
            self.setup_lines()

    def set_line_paths(self):
        self.set_line_data_path()
        self.set_line_sizes_path()

    def set_line_data_path(self):
        file_name = (
            "LineData__"
            f"Name_{self.name}__"
            f"Size_{self.config.array_size}__"
            f"PinCount_{self.config.pin_count}.npy")
        self.line_data_path = os.path.join(self.folder_path, file_name)

    def set_line_sizes_path(self):
        file_name = (
            "LineSizes__"
            f"Name_{self.name}__"
            f"Size_{self.config.array_size}__"
            f"PinCount_{self.config.pin_count}.npy")
        self.line_sizes_path = os.path.join(self.folder_path, file_name)

    def set_lines_from_file(self):
        print("Loading line data")
        line_data = np.load(self.line_data_path, allow_pickle=False)
        sizes = np.load(self.line_sizes_path, allow_pickle=False)
        for line, (start, end) in zip(self.lines, sizes):
            line.array = unpack(line_data[start:end])

    def set_lines_from_new(self):
        print("Generating line data")
        self.set_meshgrid()
        self.generate_line_arrays()
        self.save_lines()

    def generate_line_arrays(self):
        for line in self.lines:
            line.set_array()

    def save_lines(self):
        self.save_lines_data()
        self.save_lines_sizes()

    def save_lines_data(self):
        arrays = [pack(*line.array) for line in self.lines]
        line_arrays = np.concatenate(arrays, axis=1)
        np.save(self.line_data_path, line_arrays, allow_pickle=False)

    def save_lines_sizes(self):
        sizes = [0] + [line.array[1].size for line in self.lines]
        sizes = np.cumsum(sizes)
        sizes = np.stack((sizes[:-1], sizes[1:]), axis=1)
        np.save(self.line_sizes_path, sizes, allow_pickle=False)
        

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
            return self.unserialise([255, 255, 255] - array)

    def get_unsparse(indexes, values, null=0):
        array = np.ones(self.serial_size, 3) * null
        array[indexes, :] = values
        return array
        
    def save_array(self, array, name):
        array = self.ensure_unserialised(array)
        image = get_image_from_array(array)
        new_size = int(np.ceil(1000 / image.size[0]) * image.size[0])
        image = image.resize((new_size, new_size), resample=Image.BOX)
        path = os.path.join(self.folder_path, f"{name}.png")
        image.save(path)

    def plot(self, data):
        plt.plot(data)
        plt.show()

    def get_path_string(self):
        path_string = (
            f"Repository path: {self.repository_path}\n"
            f"Folder path: {self.folder_path}\n"
            f"Source image path: {self.source_path}\n")
        return path_string

    def __str__(self):
        string = f"{self.get_path_string()}"
        return string





















