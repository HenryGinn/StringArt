import matplotlib.pyplot as plt
import numpy as np

from art import Art

#art = Art("BirdImage", "BirdImage.png")
art = Art("Test2", "BirdImage.png")
#art.configure(force=False)
art.set_lines()
a = art.least_squares
art.least_squares.execute()
