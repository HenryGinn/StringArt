import tkinter as tk

from PIL import Image, ImageTk


class SetupPosition():

    def __init__(self, display):
        self.display = display
        self.art = display.art

    def setup_position(self):
        self.display_image()

    def display_image(self):
        PIL_figure = Image.open(self.art.source_path)
        tkinter_figure = ImageTk.PhotoImage(PIL_figure)
        label = tk.Label(image=tkinter_figure)
        label.image = tkinter_figure
        label.place(x=100, y=300)
