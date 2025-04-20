from PIL import Image


def resize_figure(image, width, height):
    resized_figure = image.resize(
        (width, height), resample=Image.BOX)
    return resized_figure
