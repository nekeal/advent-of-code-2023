class Matrix:
    def __init__(self, matrix: list[str]):
        self.matrix = matrix

    @property
    def height(self):
        return len(self.matrix)

    @property
    def width(self):
        return len(self.matrix[0])
