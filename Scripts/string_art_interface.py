"""
Figure:
    The source being converted to art when handled as an array
    of pixels. This is where manipulations are done.
Art:
    The whole output: the square containing the circle of pins.
Image:
    The part of the art where the source figure is displayed.
    This is used in the context of the display only,
"""


from art import Art

art = Art("BirdImage", "BirdImage.png")
#art.setup_position()
art.set_pixel_array()
