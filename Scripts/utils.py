import numpy as np
from PIL import Image


def resize_figure(image, width, height):
    resized_figure = image.resize(
        (width, height), resample=Image.BOX)
    return resized_figure

def get_image_from_array(array):
    array = np.where(np.isnan(array), 0, array)
    image = Image.fromarray(np.uint8(array))
    return image

def print_help(obj):
    for i in dir(obj):
        if i != "__array_interface__":
            print(i, getattr(obj, i))
            help(getattr(obj, i))
            print("")
