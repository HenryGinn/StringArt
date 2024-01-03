import tkinter as tk

from hgutilities import defaults


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
        self.window_centre_x = self.window_width // 2
        self.window_centre_y = self.window_height // 2

    def setup_window(self):
        self.root.title(self.art.name)
        self.root.geometry(f"{self.window_width}x{self.window_height}+0+0")

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.configure(bg=self.background_colour)
        self.canvas.pack()

defaults.load(Display)
