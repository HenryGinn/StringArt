import tkinter as tk

from hgutilities import defaults

from setup_position import SetupPosition


class Display():

    def __init__(self, art, **kwargs):
        self.art = art
        defaults.kwargs(self, kwargs)
        self.create_window()
    
    def create_window(self):
        self.root = tk.Tk()
        self.set_window_sizes()
        self.setup_window()
        self.setup_canvas()

    def set_window_sizes(self):
        self.window_width = int(self.root.winfo_screenheight())
        self.window_height = int(self.root.winfo_screenheight())

    def setup_window(self):
        self.root.title(self.art.name)
        self.root.geometry(f"{self.window_width}x{self.window_height}+0+0")

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.configure(bg=self.background_colour)
        self.canvas.pack()

    def setup_position(self):
        self.setup_position_obj = SetupPosition(self)
        self.setup_position_obj.setup_position()

defaults.load(Display)