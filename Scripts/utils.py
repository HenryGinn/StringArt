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

def get_values_indexes(array, null=0):
    non_trivial = np.any(array != null, axis=1)
    indexes = np.nonzero(non_trivial)[0].astype("int32")
    values = array[indexes, :]
    values_indexes = {"Values": values, "Indexes": indexes}
    return values_indexes

# Uses a formula from:
# https://en.wikipedia.org/wiki/Alpha_compositing#Description
# Simplified as the overall image is always opague so alpha_o = 1 always.

def add(color_a, alpha_a, array_b):
    color_b = array_b[:, :3]
    alpha_b = array_b[:, [3]]
    alpha_over = np.ones(alpha_a.shape)
    color_over = (color_a*alpha_a + color_b*alpha_b*(1 - alpha_a))
    array_over = np.concat((color_over, alpha_over), axis=1)
    return array_over



















