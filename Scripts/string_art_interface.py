import matplotlib.pyplot as plt
import numpy as np

from art import Art

#art = Art("BirdImage", "BirdImage.png")
#art = Art("Test2", "BirdImage.png")
art = Art("Test", "BirdImage.png")
art.configure(force=False)
#art.setup_lines(force=False)
art.setup_lines(force=True)
#art.save_array(art.lines[5].array, "Test")
b = art.initialise_greedy()
art.greedy.execute()
