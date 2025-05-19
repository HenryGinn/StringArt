import numpy as np


class Greedy():

    def __init__(self, art):
        self.art = art
        self.history = []
        self.start = {color: 0 for color in art.colors}
        self.array = np.zeros(self.art.source_array.shape)

    def execute(self):
        improved = self.initialise_execution()
        while improved:
            improved = self.iterate()
        self.art.save_array(self.array, "Output")

    def initialise_execution(self):
        print("Solving via greedy algorithm")
        self.current_best = np.linalg.norm(self.array - self.art.source_array)
        return True

    def iterate(self):
        lines = self.get_lines()
        self.set_differences(lines)
        line_to_add = min(self.differences, key=self.differences.get)
        improved = self.update_state(line_to_add)
        return improved

    def get_lines(self):
        lines = [
            line for color in self.art.colors
            for line in self.art.line_lookup[(self.start[color], color)]]
        return lines

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

    def update_state(self, line_to_add):
        improved = self.differences[line_to_add] < self.current_best
        self.current_best = self.differences[line_to_add]
        self.add_next_line(line_to_add)
        self.start[line_to_add.color] = line_to_add.lookup[self.start[line_to_add.color]]
        return improved

    def add_next_line(self, line_to_add):
        values, indexes = line_to_add.array
        self.array[indexes] += values
        action = (line_to_add, self.differences[line_to_add])
        self.history.append(action)
