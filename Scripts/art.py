import os
import sys

class Art():

    def __init__(self, folder_name, source_name):
        self.process_path_data(folder_name, source_name)

    def process_path_data(self, folder_name, source_name):
        self.repository_path = os.path.split(sys.path[0])[0]
        self.folder_path = os.path.join(self.repository_path, folder_name)
        self.source_path = os.path.join(self.folder_path, source_name)

    def get_path_string(self):
        path_string = (f"Repository path: {self.repository_path}\n"
                       f"Folder path: {self.folder_path}\n"
                       f"Source image path: {self.source_path}\n")
        return path_string

    def __str__(self):
        string = f"{self.get_path_string()}"
        return string