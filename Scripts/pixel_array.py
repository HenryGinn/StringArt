import os

import numpy as np
from hgutilities import defaults
from PIL import Image

from utils import (
    resize_figure)


class PixelArray():

    def __init__(self, art):
        self.art = art
        self.array = self.art.config.get_blank_array()

    def set_array(self):
        self.art.save_array(self.array, "Output")































