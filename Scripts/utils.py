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
    values = array[indexes, :].astype("uint8")
    return values, indexes

def pack(values, indexes):
    arrays = (indexes.reshape(-1, 1), values)
    sparse = np.concatenate(arrays, axis=1)
    return sparse

def unpack(sparse):
    values = sparse[:, [1, 2, 3]]
    indexes = sparse[:, 0].reshape(-1)
    return values, indexes




















