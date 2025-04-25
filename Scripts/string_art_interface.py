import matplotlib.pyplot as plt
import numpy as np

from art import Art

#art = Art("BirdImage", "BirdImage.png")
art = Art("Test", "BirdImage.png")
#art.configure(force=False)
art.set_lines()
art.least_squares.execute()
