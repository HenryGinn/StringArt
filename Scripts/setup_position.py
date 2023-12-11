import tkinter as tk

from PIL import Image, ImageTk


class SetupPosition():

    def __init__(self, display):
        self.display = display
        self.art = display.art

    def setup_position(self):
        self.set_initial_values()
        self.display_image()

    def set_initial_values(self):
        self.x_position = self.display.window_width / 2
        self.y_position = self.display.window_height / 2
        self.figure_width = int(self.display.window_width / 3)

    def display_image(self):
        PIL_figure = Image.open(self.art.source_path)
        PIL_figure = self.resize_figure(PIL_figure)
        tkinter_figure = ImageTk.PhotoImage(PIL_figure)
        label = tk.Label(image=tkinter_figure)
        label.image = tkinter_figure
        self.place_figure(label, PIL_figure)

    def resize_figure(self, PIL_figure):
        self.figure_height = int(self.figure_width * PIL_figure.height/PIL_figure.width)
        PIL_figure = PIL_figure.resize((self.figure_width, self.figure_height))
        return PIL_figure

    def place_figure(self, label, PIL_figure):
        x_position = self.x_position - PIL_figure.width / 2
        y_position = self.y_position - PIL_figure.height / 2
        label.place(x=x_position, y=y_position)
