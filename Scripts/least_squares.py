import numpy as np


class LeastSquares():

    def __init__(self, art):
        self.art = art

    def execute(self):
        self.art.ensure_lines_setup()
        print("Solving via linear least squares")
        # Reshaping the line matrices from n x 3 to be vectors so they
        # can be stacked together into an 3n x m matrix.
        self.matrix = [line.array.reshape(-1) for line in self.art.lines]
        self.matrix = np.stack(self.matrix, axis=1)
        self.target = self.art.source_array.reshape(-1)
        self.coefficients, self.residuals, _, _ = np.linalg.lstsq(self.matrix, self.target)
        self.array = np.matmul(self.matrix, self.coefficients).reshape(-1, 3)
        self.art.save_array(self.array, "LeastSquares")
