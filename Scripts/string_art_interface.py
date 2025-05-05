import matplotlib.pyplot as plt
import numpy as np

from art import Art

#art = Art("BirdImage", "BirdImage.png")
art = Art("Test", "BirdImage.png")
#art.configure(force=False)
#art.setup_lines()
a = art.greedy
art.greedy.execute()
