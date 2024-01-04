from hgutilities import defaults


class PixelArray():

    def __init__(self, art):
        self.art = art
        self.inherit_from_setup_position()

    def inherit_from_setup_position(self):
        kwargs = ["figure", "pin_radius"
                  "x_position", "y_position",
                  "image_width", "image_height"]
        defaults.inherit(self, self.art.setup_position_obj, kwargs)

    def resize_figure(self):
        resize = self.art.setup_position_obj.resize_figure
        self.figure = resize(self.figure)

    def set_pixel_array(self):
        for i in dir(self.figure):
            if i != "__array_interface__":
                print(i, getattr(self.figure, i))
