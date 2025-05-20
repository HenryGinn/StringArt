import numpy as np

from utils import add


class Greedy():

    def __init__(self, art):
        self.art = art
        self.history = []
        self.past_lines = set([])
        self.start = {color: 0 for color in art.colors}
        self.array = (np.ones(self.art.source_array.shape)
                      * self.art.config.background_color)

    def execute(self):
        improved = self.initialise_execution()
        while improved:
            self.iterate()
            if self.counter % 100 == 0:
                self.art.save_array(self.array, f"Iteration_{self.counter:04}")
                improved = False
            self.counter += 1
        self.art.save_array(self.array, "Output")

    def initialise_execution(self):
        print("Solving via greedy algorithm")
        self.current_best = np.linalg.norm(self.array - self.art.source_array)
        self.counter = 1
        return True

    def iterate(self):
        colored_lines = self.get_lines()
        self.set_differences(colored_lines)
        line, color = min(self.differences, key=self.differences.get)
        improved = self.update_state(line, color)
        return improved

    def get_lines(self):
        lines = [
            (line, color) for color in self.art.colors
            for line in self.art.line_lookup[self.start[color]]
            if line not in self.past_lines]
        return lines

    def set_differences(self, colored_lines):
        self.differences = {
            (line, color): self.get_norm(line, color)
            for (line, color) in colored_lines}

    def get_norm(self, line, color):
        array = self.get_array(line.array, color)
        array -= self.art.source_array
        norm = np.linalg.norm(array)
        return norm

    def get_array(self, sparse, color):
        array = self.array.copy()
        indexes = sparse["Indexes"]
        values = sparse["Values"]
        array[indexes] = add(color, values, array[indexes, :])
        return array

    def update_state(self, line, color):
        improved = self.differences[(line, color)] < self.current_best
        self.current_best = self.differences[(line, color)]
        self.add_next_line(line, color)
        self.start[color] = line.lookup[self.start[color]]
        return improved

    def add_next_line(self, line, color):
        self.array = self.get_array(line.array, color)
        self.past_lines = self.past_lines.union(set([(line, color)]))
        self.history += [self.differences[(line, color)]]
