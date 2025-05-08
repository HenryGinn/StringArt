import numpy as np


class Greedy():

    def __init__(self, art):
        self.art = art
        self.sequence = []
        self.start = 0
        self.array = np.zeros(self.art.source_array.shape)

    def execute(self):
        print("Solving via greedy algorithm")
        for i in range(500):
            self.iteration()
            if i % 20 == 0:
                self.art.save_array(self.array, f"Iteration_{i:03}")

    def iteration(self):
        lines = self.art.line_lookup[self.start]
        self.set_differences(lines)
        line_to_add = min(self.differences, key=self.differences.get)
        self.array += line_to_add.array
        self.sequence.append((line_to_add, self.differences[line_to_add]))
        self.start = line_to_add.lookup[self.start]

    def set_differences(self, lines):
        self.differences = {
            line: np.linalg.norm(
                self.array + line.array - self.art.source_array)
            for line in lines}
