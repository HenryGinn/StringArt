import os
import json
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk

from int_input import get_int_input


class SetupPosition():

    def __init__(self, display_obj):
        self.display_obj = display_obj
        self.art = display.art
        self.figure = Image.open(self.art.source_path)
        self.set_path()
        self.set_modify_inputs()

    def set_path(self):
        self.path = os.path.join(self.art.folder_path,
                                 "Position Configuration.json")

    def setup_position(self):
        self.user_not_satisfied = True
        if os.path.exists(self.path):
            self.path_already_exists()
        else:
            self.do_setup_position_from_new()

    def path_already_exists(self):
        try:
            self.display_image_from_path()
        except:
            self.path_exists_but_fail()

    def path_exists_but_fail(self):
        print(("A position configuration file exists but data could not"
               "be extracted. Recreating new position configuration file"
               f"\n\nFile path:\n{self.path}"))
        self.do_setup_position_from_new()

    def display_image_from_path(self):
        self.load_configuration_from_file()
        self.display_configuration()
        self.update_user_not_satisfied()
        self.do_setup_position()

    def load_configuration_from_file(self):
        with open(self.path, "r") as file:
            self.config = json.load(file)
        self.extract_from_configuration_dict()

    def extract_from_configuration_dict(self):
        self.extract_image_configuration()
        self.extract_pin_configuration()

    def extract_image_configuration(self):
        self.x_position = self.config["Image Properties"]["x"]
        self.y_position = self.config["Image Properties"]["y"]
        self.image_width = self.config["Image Properties"]["Width"]
        self.image_height = self.config["Image Properties"]["Height"]

    def extract_pin_configuration(self):
        self.pin_radius = self.config["Pin Circle"]["Radius"]
        self.pin_count = self.config["Pin Circle"]["Count"]

    def do_setup_position_from_new(self):
        self.set_initial_values()
        self.display_configuration()
        self.do_setup_position()

    def do_setup_position(self):
        while self.user_not_satisfied:
            self.modify_configuration()
            self.update_user_not_satisfied()
        self.save_new_configuration()

    def set_initial_values(self):
        self.set_initial_image_config()
        self.set_initial_pin_config()
        self.set_initial_process_config()

    def set_initial_image_config(self):
        self.x_position = self.display.window_width / 2
        self.y_position = self.display.window_height / 2
        self.image_width = int(self.display.window_width / 3)
        aspect_ratio = self.figure.height / self.figure.width
        self.image_height = int(self.image_width * aspect_ratio)

    def set_initial_pin_config(self):
        self.pin_radius = 0.6 * max(self.image_width,
                                    self.image_height)
        self.pin_count = 11

    def modify_configuration(self):
        self.modify()
        self.display_configuration()
    

    def display_configuration(self):
        self.display_image()
        self.display_pins()
        self.art.update()

    def display_image(self):
        PIL_figure = self.resize_figure()
        tkinter_figure = ImageTk.PhotoImage(PIL_figure)
        self.image_label = tk.Label(image=tkinter_figure)
        self.image_label.image = tkinter_figure
        self.place_figure(PIL_figure)

    def resize_figure(self):
        resized_figure = self.figure.resize((self.image_width,
                                             self.image_height))
        return resized_figure

    def place_figure(self, PIL_figure):
        #self.delete_old_figure()
        x_position = self.x_position - PIL_figure.width / 2
        y_position = self.y_position - PIL_figure.height / 2
        self.image_label.place(x=x_position, y=y_position)

    def delete_old_figure(self):
        self.image_label.test

    def display_pins(self):
        self.set_pin_positions()
        self.delete_pin_widgets()
        self.draw_pins()

    def set_pin_positions(self):
        angles = np.linspace(0, 2*np.pi, num=self.pin_count, endpoint=False)
        self.set_pin_positions_x(angles)
        self.set_pin_positions_y(angles)

    def set_pin_positions_x(self, angles):
        self.pin_positions_x = (self.display_obj.window_centre_x +
                                self.pin_radius * np.cos(angles))

    def set_pin_positions_y(self, angles):
        self.pin_positions_y = (self.display_obj.window_centre_y +
                                self.pin_radius * np.sin(angles))

    def delete_pin_widgets(self):
        if hasattr(self, "pins"):
            pass

    def draw_pins(self):
        pass
    

    def update_user_not_satisfied(self):
        prompt = ("Is this configuration satisfactory?\n"
                  "1: Yes\n2: No\n")
        response = get_int_input(prompt, lower_bound=1, upper_bound=2)
        self.user_not_satisfied = [False, True][response - 1]

    def set_modify_inputs(self):
        self.set_modify_functions()
        self.set_modify_prompt()

    def set_modify_functions(self):
        self.modify_functions = [self.modify_position_x,
                                 self.modify_position_y,
                                 self.modify_image_width,
                                 self.modify_image_height,
                                 self.modify_pin_radius,
                                 self.modify_pin_count]

    def set_modify_prompt(self):
        self.prompt = ("\nWhat property do you want to modify?\n"
                       "1: X position\n"
                       "2: Y position\n"
                       "3: Image width\n"
                       "4: Image height\n"
                       "5: Pin circle radius\n"
                       "6: Number of pins\n")

    def modify(self):
        modify_function_index = get_int_input(self.prompt,
                                              lower_bound=1,
                                              upper_bound=6) - 1
        modify_function = self.modify_functions[modify_function_index]()

    def modify_position_x(self):
        self.modify_variable("x position", "x_position")

    def modify_position_y(self):
        self.modify_variable("y position", "x_position")

    def modify_image_width(self):
        aspect_ratio = self.figure.height / self.figure.width
        self.modify_variable("image width", "image_width")
        self.image_height = int(self.image_width * aspect_ratio)

    def modify_image_height(self):
        aspect_ratio = self.figure.height / self.figure.width
        self.modify_variable("image height", "image_height")
        self.image_weight = int(self.image_height / aspect_ratio)

    def modify_pin_radius(self):
        self.modify_variable("pin circle radius", "pin_radius")

    def modify_pin_count(self):
        self.modify_variable("pin count", "pin_count")

    def modify_variable(self, variable_description, attribute_name):
        old_value = getattr(self, attribute_name)
        prompt = (f"\nThe current value of {variable_description} is "
                  f"{round(old_value)}\n"
                  "What would you like to change it to?\n")
        new_value = get_int_input(prompt, lower_bound=1)
        setattr(self, attribute_name, new_value)


    def save_new_configuration(self):
        self.set_config()
        with open(self.path, "w+") as file:
            json.dump(self.config, file, indent=2)

    def set_config(self):
        self.config = {}
        self.set_config_image_properties()
        self.set_config_pin_circle()

    def set_config_image_properties(self):
        properties_dict = {"x": self.x_position,
                           "y": self.y_position,
                           "Width": self.image_width,
                           "Height": self.image_height}
        self.config["Image Properties"] = properties_dict

    def set_config_pin_circle(self):
        pin_dict = {"Radius": self.pin_radius,
                    "Count": self. pin_count}
        self.config["Pin Circle"] = pin_dict
