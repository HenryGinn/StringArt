import numpy as np


class Greedy():

    def __init__(self, art):
        self.art = art
        self.sequence = []
        self.start = 0
        self.array = np.zeros(self.art.source_array.shape)

    def execute(self):
        print("Solving via greedy algorithm")
        self.current_best = np.linalg.norm(self.array - self.art.source_array)
        improved = True
        self.results = []
        while improved:
            improved = self.iteration()
            self.results.append(self.current_best)
        self.art.save_array(self.array, "Output")

    def iteration(self):
        lines = self.art.line_lookup[self.start]
        self.set_differences(lines)
        line_to_add = min(self.differences, key=self.differences.get)
        improved = self.differences[line_to_add] < self.current_best
        self.current_best = self.differences[line_to_add]
        values, indexes = line_to_add.array
        self.array[indexes] += values
        self.sequence.append((line_to_add, self.differences[line_to_add]))
        self.start = line_to_add.lookup[self.start]
        return improved

    def set_differences(self, lines):
        self.differences = {
            line: np.linalg.norm(
                self.get_array(*line.array))
            for line in lines}

    def get_array(self, values, indexes):
        array = self.array.copy()
        array[indexes] = (array[indexes] + values)/2
        array -= self.art.source_array
        return array
