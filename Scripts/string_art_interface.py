import matplotlib.pyplot as plt
import numpy as np

from art import Art

art = Art("BirdImage", "BirdImage.png")
#art = Art("Test", "BirdImage.png")
#art = Art("Test2", "BirdImage.png")
art.configure(force=False)
lines = art.lines
l = lines[0]
art.compute_lines()
