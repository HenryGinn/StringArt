import numpy as np


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
            if self.counter % 10 == 0:
                self.art.save_array(self.array, f"Iteration_{self.counter:04}")
                input()
            self.counter += 1
            self.iterate()
        self.art.save_array(self.array, "Output")

    def initialise_execution(self):
        print("Solving via greedy algorithm")
        self.current_best = np.linalg.norm(self.array - self.art.source_array)
        self.counter = 0
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
            for line in self.art.line_lookup[(self.start[color], color)]
            if line not in self.past_lines]
        return lines

    def set_differences(self, lines):
        self.differences = {
            line: self.get_norm(line)
            for line in lines}

    def get_norm(self, line):
        array = self.get_array(line)
        array -= self.art.source_array
        norm = np.linalg.norm(array)
        return norm

    def get_array(self, line):
        values, indexes = line.array
        array = self.array.copy()
        array[indexes] = array[indexes] + values
        return array

    def update_state(self, line_to_add):
        improved = self.differences[line_to_add] < self.current_best
        self.current_best = self.differences[line_to_add]
        self.add_next_line(line_to_add)
        self.start[line_to_add.color] = line_to_add.lookup[self.start[line_to_add.color]]
        return improved

    def add_next_line(self, line_to_add):
        self.array = self.get_array(line_to_add)
        self.past_lines = self.past_lines.union(set([line_to_add]))
        self.history += [self.differences[line_to_add]]
