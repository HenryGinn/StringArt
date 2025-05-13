import matplotlib.pyplot as plt
import numpy as np

from art import Art

#art = Art("BirdImage", "BirdImage.png")
art = Art("Test2", "BirdImage.png")
art.set_physical_parameters(thread_width=0.12, diameter=0.6)
#art.configure(force=False)
art.setup_lines(force=False)
#art.setup_lines(force=True)
a = art.lines[0]
#art.save_array(a.array, "Line")
#b = art.initialise_greedy()
#art.greedy.execute()
