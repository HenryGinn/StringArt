import numpy as np


class Greedy():

    def __init__(self, art):
        self.art = art

    def execute(self):
        self.art.ensure_lines_setup()
        print("Solving via greedy algorithm")
        self.pin_1 = 0
