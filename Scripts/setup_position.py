import os
import json
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk

from int_input import get_int_input
from color_input import get_color_input


class SetupPosition():

    def __init__(self, art):
        self.art = art
        self.display_obj = art.display_obj
        self.figure = Image.open(self.art.source_path)
        self.set_path()
        self.set_modify_inputs()

    def set_path(self):
        self.path = os.path.join(
            self.art.folder_path,
            "PositionConfig.json")

    def setup_position(self, force):
        self.process_force_arg(force)
        self.set_config_file()
        self.do_setup_position()
        self.art.position_setup = True

    def process_force_arg(self, force):
        self.user_not_satisfied = True
        self.force = force

    def set_config_file(self):
        if os.path.exists(self.path):
            self.path_already_exists()
        else:
            self.do_setup_position_from_new()

    def path_already_exists(self):
        try:
            self.try_load_config_from_file()
        except:
            self.path_exists_but_fail()

    def try_load_config_from_file(self):
        self.load_config_from_file()
        self.user_not_satisfied = self.force
        if self.force:
            self.display_config()

    def path_exists_but_fail(self):
        print(("A position configuration file exists but data could not "
               "be extracted.\n"
               "A new position configuration file will be created\n\n"
               f"File path:\n{self.path}"))
        self.do_setup_position_from_new()

    def load_config_from_file(self):
        with open(self.path, "r") as file:
            self.config = json.load(file)
        self.extract_from_config_dict()

    def extract_from_config_dict(self):
        self.extract_image_config()
        self.extract_pin_config()
        self.extract_color_config()

    def extract_image_config(self):
        self.x_position = self.config["Image Properties"]["x"]
        self.y_position = self.config["Image Properties"]["y"]
        self.image_width = self.config["Image Properties"]["Width"]
        self.image_height = self.config["Image Properties"]["Height"]

    def extract_pin_config(self):
        self.pin_radius = self.config["Pin Circle"]["Radius"]
        self.pin_count = self.config["Pin Circle"]["Count"]

    def extract_color_config(self):
        self.background_color = self.config["Color"]["Background"]
        self.pin_color = self.config["Color"]["Pins"]

    def do_setup_position_from_new(self):
        self.set_initial_values()
        self.display_config()

    def do_setup_position(self):
        if self.user_not_satisfied:
            self.ensure_user_satisfied()
            self.save_new_config()

    def ensure_user_satisfied(self):
        while self.user_not_satisfied:
            self.modify_config()
            self.update_user_not_satisfied()

    def set_initial_values(self):
        self.set_initial_image_config()
        self.set_initial_pin_config()
        self.set_initial_color_config()

    def set_initial_image_config(self):
        self.x_position = self.display_obj.window_centre_x
        self.y_position = self.display_obj.window_centre_y
        self.image_width = int(self.display_obj.window_width * 0.5)
        aspect_ratio = self.figure.height / self.figure.width
        self.image_height = int(self.image_width * aspect_ratio)

    def set_initial_pin_config(self):
        self.pin_radius = 0.7 * max(self.image_width,
                                    self.image_height)
        self.pin_count = 11

    def set_initial_color_config(self):
        self.background_color = "white"
        self.pin_color = "#FF0000"
    

    def display_config(self):
        self.display_background_circle()
        self.display_image()
        self.display_pins()
        self.art.update()

    def display_background_circle(self):
        self.remove_background_circle()
        self.background_circle = (
            self.create_circle(self.display_obj.window_centre_x,
                               self.display_obj.window_centre_y,
                               self.pin_radius,
                               self.background_color))

    def remove_background_circle(self):
        if hasattr(self, "background_circle"):
            self.display_obj.canvas.delete(self.background_circle)

    def display_image(self):
        PIL_figure = self.resize_figure()
        tkinter_image = ImageTk.PhotoImage(PIL_figure)
         # Stop garbage collection
        self.display_obj.root.tkinter_image = tkinter_image
        self.place_image(tkinter_image)
        
    def resize_figure(self):
        resized_figure = self.figure.resize(
            (self.image_width, self.image_height))
        return resized_figure

    def place_image(self, tkinter_image):
        self.display_obj.canvas.create_image(
            self.x_position, self.y_position,
            anchor="center", image=tkinter_image)

    def display_pins(self):
        self.set_pin_positions()
        self.delete_pins()
        self.draw_pins()

    def set_pin_positions(self):
        angles = np.linspace(0, 2*np.pi, num=self.pin_count, endpoint=False)
        self.set_pin_positions_x(angles)
        self.set_pin_positions_y(angles)

    def set_pin_positions_x(self, angles):
        self.pin_positions_x = (self.display_obj.window_centre_x +
                                self.pin_radius * np.cos(angles))
        self.art.pin_x = self.pin_positions_x

    def set_pin_positions_y(self, angles):
        self.pin_positions_y = (self.display_obj.window_centre_y +
                                self.pin_radius * np.sin(angles))
        self.art.pin_y = self.pin_positions_y

    def delete_pins(self):
        if hasattr(self, "pins"):
            for pin in self.pins:
                self.display_obj.canvas.delete(pin)

    def draw_pins(self):
        r = 2
        pin_positions = zip(self.pin_positions_x, self.pin_positions_y)
        self.pins = [self.create_circle(x, y, r, self.pin_color)
                     for x, y in pin_positions]

    def create_circle(self, x, y, r, color):
        circle = self.display_obj.canvas.create_oval(
            x-r, y-r, x+r, y+r, fill=color, outline=color)
        return circle
    

    def update_user_not_satisfied(self):
        self.display_config()
        prompt = ("\nIs this configuration satisfactory?\n"
                  "1: Yes\n2: No\n")
        response = get_int_input(prompt, lower_bound=1, upper_bound=2)
        self.user_not_satisfied = [False, True][response - 1]

    def set_modify_inputs(self):
        self.set_modify_functions()
        self.set_modify_prompt()

    def set_modify_functions(self):
        self.modify_functions = [
            self.modify_position_x,
            self.modify_position_y,
            self.modify_image_width,
            self.modify_image_height,
            self.modify_pin_radius,
            self.modify_pin_count,
            self.modify_background_color,
            self.modify_pin_color,
            self.modify_nothing]

    def set_modify_prompt(self):
        self.prompt = (
            "\nWhat property do you want to modify?\n"
            "1: X position\n"
            "2: Y position\n"
            "3: Image width\n"
            "4: Image height\n"
            "5: Pin circle radius\n"
            "6: Number of pins\n"
            "7: Background color\n"
            "8: Pin color\n"
            "9: Nothing\n")

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

    def modify_image_width(self):
        aspect_ratio = self.figure.height / self.figure.width
        self.modify_int_variable("image width", "image_width")
        self.image_height = int(self.image_width * aspect_ratio)

    def modify_image_height(self):
        aspect_ratio = self.figure.height / self.figure.width
        self.modify_int_variable("image height", "image_height")
        self.image_width = int(self.image_height / aspect_ratio)

    def modify_pin_radius(self):
        self.modify_int_variable("pin circle radius", "pin_radius")

    def modify_pin_count(self):
        self.modify_int_variable("pin count", "pin_count")

    def modify_background_color(self):
        self.modify_color_variable("background color",
                                    "background_color")

    def modify_pin_color(self):
        self.modify_color_variable("pin color", "pin_color")

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


    def save_new_config(self):
        self.set_config()
        with open(self.path, "w+") as file:
            json.dump(self.config, file, indent=2)

    def set_config(self):
        self.config = {}
        self.set_config_image_properties()
        self.set_config_pin_circle()
        self.set_config_colors()

    def set_config_image_properties(self):
        properties_dict = {"x": self.x_position,
                           "y": self.y_position,
                           "Width": self.image_width,
                           "Height": self.image_height}
        self.config["Image Properties"] = properties_dict

    def set_config_pin_circle(self):
        pin_dict = {"Radius": self.pin_radius,
                    "Count": self.pin_count,
                    "Color": self.pin_color}
        self.config["Pin Circle"] = pin_dict

    def set_config_colors(self):
        color_dict = {"Background": self.background_color,
                       "Pins": self.pin_color}
        self.config["Color"] = color_dict
