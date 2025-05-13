import os
import json
import tkinter as tk
import traceback

import matplotlib.colors as mcol
import numpy as np
from PIL import Image, ImageTk
from resizeimage.resizeimage import resize_contain

from int_input import get_int_input
from color_input import get_color_input
from utils import (
    resize_figure)


class Config():

    def __init__(self, art):
        self.art = art
        self.set_path()
        self.initialise_figure()
        self.set_modify_inputs()

    def set_path(self):
        self.path = os.path.join(
            self.art.folder_path,
            "PositionConfig.json")

    def initialise_figure(self):
        self.figure = Image.open(self.art.source_path)
        self.figure = self.figure.convert(mode="RGBA")
        self.figure_size = max(self.figure.width, self.figure.height)
        size = (self.figure_size, self.figure_size)
        self.figure = resize_contain(self.figure, size)


    # Main logic

    def configure(self, force):
        self.process_force_arg(force)
        self.set_config_file()
        self.do_configure()
        self.art.configured = True

    def process_force_arg(self, force):
        self.user_not_satisfied = True
        self.force = force

    def set_config_file(self):
        if os.path.exists(self.path):
            self.path_already_exists()
        else:
            self.set_initial_values()

    def path_already_exists(self):
        try:
            self.try_load_config_from_file()
        except Exception:
            self.path_exists_but_fail()

    def try_load_config_from_file(self):
        self.load_config_from_file()
        self.user_not_satisfied = self.force

    def path_exists_but_fail(self):
        print(("A position configuration file exists but data could not "
               "be extracted.\n"
               "A new position configuration file will be created\n\n"
               f"File path:\n{self.path}\n\n"
               f"{traceback.format_exc()}"))
        self.set_initial_values()

    def do_configure(self):
        self.set_source_array()
        if self.user_not_satisfied:
            self.ensure_user_satisfied()
            self.save_new_config()

    def ensure_user_satisfied(self):
        while self.user_not_satisfied:
            self.save_source()
            self.modify_config()
            self.update_user_not_satisfied()

    def update_user_not_satisfied(self):
        self.save_source()
        prompt = ("\nIs this configuration satisfactory?\n"
                  "1: Yes\n2: No\n")
        response = get_int_input(prompt, lower_bound=1, upper_bound=2)
        self.user_not_satisfied = [False, True][response - 1]


    # Loading configuration

    def load_config_from_file(self):
        with open(self.path, "r") as file:
            self.config = json.load(file)
        self.extract_from_config_dict()

    def extract_from_config_dict(self):
        self.extract_config_other()
        self.extract_image_config()
        self.array_size_updated()
        self.set_pins()

    def extract_config_other(self):
        self.array_size = self.config["Array Size"]
        self.background_color = self.config["Background Color"]
        self.pin_count = self.config["Pin Count"]

    def extract_image_config(self):
        self.x_position = self.config["Image Properties"]["x"]
        self.y_position = self.config["Image Properties"]["y"]
        self.image_size = self.config["Image Properties"]["Size"]


    # Initialisation of configuration

    def set_initial_values(self):
        self.set_initial_array_size()
        self.set_initial_image_config()
        self.set_initial_pin_config()
        self.set_initial_color_config()

    def set_initial_array_size(self):
        self.array_size = 1000
        self.array_size_updated()

    def set_initial_image_config(self):
        self.image_size = int(self.array_size * 0.7)
        self.x_position = int((self.array_size - self.image_size) / 2)
        self.y_position = int((self.array_size - self.image_size) / 2)

    def set_initial_pin_config(self):
        self.pin_count = 100
        self.set_pins()

    def set_initial_color_config(self):
        self.background_color = "white"

    def set_pins(self):
        angles = np.linspace(0, 2*np.pi, num=self.pin_count, endpoint=False)
        pin_x = (self.array_size - 1) * 0.4999 * (1 + np.cos(angles))
        pin_y = (self.array_size - 1) * 0.4999 * (1 + np.sin(angles))
        self.art.pins = np.array([pin_x, pin_y]).T


    # Array manipulation

    def set_source_array(self):
        self.art.source_array = self.art.blank_array.copy()
        figure_array = self.get_figure_array()
        non_transparent = self.get_non_transparant(figure_array)
        self.art.source_array = np.where(
            non_transparent, figure_array[:, :, :3], self.art.source_array)
        self.art.source_array = self.art.serialise(self.art.source_array)
    
    def get_figure_array(self):
        figure = np.array(self.figure.resize((self.image_size, self.image_size)))
        figure_array = np.zeros((self.array_size, self.array_size, 4))
        start_y = min(self.y_position, self.array_size)
        end_y = min(self.y_position + self.image_size, self.array_size)
        start_x = min(self.x_position, self.array_size)
        end_x = min(self.x_position + self.image_size, self.array_size)
        figure_array[
            start_y:end_y, start_x:end_x] = figure[:end_y - start_y, :end_x - start_x]
        return figure_array

    def get_non_transparant(self, figure_array):
        non_transparent = (figure_array[:, :, 3] > 0)[:, :, np.newaxis]
        non_transparant = np.tile(non_transparent, (1, 1, 3))
        return non_transparent

    def set_blank_array(self):
        circle_array = self.get_circle_array()
        background_array = self.get_color_array(self.background_color)
        surroundings_array = self.get_color_array("#021b34")
        self.art.blank_array = np.where(
            circle_array, background_array, surroundings_array)

    def get_circle_array(self):
        circle_array = self.get_circle_array_two_dimensions()
        circle_array = np.expand_dims(circle_array, -1)
        circle_array = np.tile(circle_array, (1, 1, 3))
        self.art.circle_indexes = np.where(circle_array[:, :, 0])
        self.art.serial_length = self.art.circle_indexes[0].size
        return circle_array

    def get_circle_array_two_dimensions(self):
        radius = (self.array_size - 1) // 2
        constructer = self.get_circle_constructer_array(radius)
        x, y = np.meshgrid(constructer, constructer)
        pixel_distance = np.sqrt(x**2 + y**2)
        circle = np.where(pixel_distance <= radius + 0.1, 1, 0)
        return circle

    def get_circle_constructer_array(self, radius):
        left = np.linspace(radius, 0, radius + 1)
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

    def array_size_updated(self):
        self.array_shape = (self.array_size, self.array_size, 3)
        self.set_blank_array()

    def save_source(self):
        self.set_source_array()
        self.art.save_array(self.art.source_array, "Source")


    # Modification of settings

    def set_modify_inputs(self):
        self.set_modify_functions()
        self.set_modify_prompt()

    def set_modify_functions(self):
        self.modify_functions = [
            self.modify_position_x,
            self.modify_position_y,
            self.modify_image_size,
            self.modify_pin_count,
            self.modify_background_color,
            self.modify_array_size,
            self.modify_nothing]

    def set_modify_prompt(self):
        self.prompt = (
            "\nWhat property do you want to modify?\n"
            "1: X position\n"
            "2: Y position\n"
            "3: Image size\n"
            "4: Number of pins\n"
            "5: Background color\n"
            "6: Array size\n"
            "7: Nothing\n")

    def modify_config(self):
        count = len(self.modify_functions)
        modify_function_index = get_int_input(self.prompt,
                                              lower_bound=1,
                                              upper_bound=count) - 1
        modify_function = self.modify_functions[modify_function_index]()

    def modify_position_x(self):
        self.modify_int_variable("x position", "x_position")

    def modify_position_y(self):
        self.modify_int_variable("y position", "y_position")

    def modify_image_size(self):
        self.modify_int_variable("image size", "image_size")

    def modify_pin_count(self):
        self.modify_int_variable("pin count", "pin_count")
        self.set_pins()

    def modify_background_color(self):
        self.modify_color_variable("background color",
                                    "background_color")

    def modify_array_size(self):
        self.modify_int_variable("array size", "array_size")
        self.array_size_updated()

    def modify_nothing(self):
        pass

    def modify_int_variable(self, variable_description, attribute_name):
        old_value = getattr(self, attribute_name)
        prompt = (f"\nThe current value of {variable_description} is "
                  f"{round(old_value)}\n"
                  "What would you like to change it to?\n")
        new_value = get_int_input(prompt, lower_bound=1)
        setattr(self, attribute_name, new_value)

    def modify_color_variable(self, variable_description, attribute_name):
        old_color = getattr(self, attribute_name)
        prompt = (f"\nThe current color of {variable_description} is "
                  f"{old_color}\n"
                  "What would you like to change it to?\n")
        new_color = get_color_input(prompt)
        setattr(self, attribute_name, new_color)


    # Saving configuration file

    def save_new_config(self):
        self.set_config()
        with open(self.path, "w+") as file:
            json.dump(self.config, file, indent=2)

    def set_config(self):
        self.config = {}
        self.set_config_other()
        self.set_config_image_properties()

    def set_config_other(self):
        self.config["Array Size"] = self.array_size
        self.config["Background Color"] = self.background_color
        self.config["Pin Count"] = self.pin_count

    def set_config_image_properties(self):
        properties_dict = {"x": self.x_position,
                           "y": self.y_position,
                           "Size": self.image_size}
        self.config["Image Properties"] = properties_dict
