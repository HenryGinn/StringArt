import matplotlib.pyplot as plt
import numpy as np

from art import Art

art = Art("BirdImage", "BirdImage.png")
art.set_physical_parameters(thread_width=0.001, diameter=0.6)
#art = Art("Test2", "BirdImage.png")
#art.configure(force=False)
art.setup_lines(force=True)
#a = art.lines[0]
#art.save_array(art.lines[0].array, "Line")
#a = art.initialise_greedy()
#art.greedy.execute()
