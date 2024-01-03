import os
import sys

from PIL import Image
from hgutilities import defaults

from display import Display
from setup_position import SetupPosition

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
        self.display_obj = Display(self, **kwargs)
        self.setup_position_obj = SetupPosition(self)

    def ensure_position_setup(self):
        if not self.position_setup:
            self.setup_position(force=False)

    def setup_position(self, force=True):
        self.setup_position_obj.setup_position(force)

    def update(self):
        self.display_obj.root.update()

    def get_path_string(self):
        path_string = (f"Repository path: {self.repository_path}\n"
                       f"Folder path: {self.folder_path}\n"
                       f"Source image path: {self.source_path}\n")
        return path_string

    def __str__(self):
        string = f"{self.get_path_string()}"
        return string


defaults.load(Art)
