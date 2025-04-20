import os
import sys

from hgutilities import defaults
from PIL import Image

from config import Config
from pixel_array import PixelArray
from utils import get_image_from_array

class Art():

    def __init__(self, folder_name, source_name, **kwargs):
        defaults.kwargs(self, kwargs)
        self.process_path_data(folder_name, source_name)
        self.set_objects(**kwargs)
        self.position_setup = False

    def process_path_data(self, folder_name, source_name):
        self.name = folder_name
        self.repository_path = os.path.split(sys.path[0])[0]
        self.folder_path = os.path.join(self.repository_path, "Data", folder_name)
        self.source_path = os.path.join(self.folder_path, source_name)

    def set_objects(self, **kwargs):
        self.config = Config(self)

    def ensure_position_setup(self):
        if not self.position_setup:
            self.setup_position(force=False)

    def setup_position(self, force=True):
        self.config.setup_position(force)
        self.source_array = self.config.source_array

    def set_pixel_array(self):
        self.ensure_position_setup()
        self.pixel_array_obj = PixelArray(self)
        self.pixel_array_obj.set_array()

    def get_path_string(self):
        path_string = (f"Repository path: {self.repository_path}\n"
                       f"Folder path: {self.folder_path}\n"
                       f"Source image path: {self.source_path}\n")
        return path_string

    def save_array(self, array, name):
        image = get_image_from_array(array)
        path = os.path.join(self.folder_path, f"{name}.png")
        image.save(path)

    def __str__(self):
        string = f"{self.get_path_string()}"
        return string


defaults.load(Art)
