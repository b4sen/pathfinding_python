# TODO: f(x) = g(x) + h(x)


class Node:
    """
    Node values:
        1: start
        2: end
        3: wall
        4: visited
        5: path
        0: empty
    """

    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []

    def __str__(self):
        neighbors = [n.val for n in self.neighbors]
        return self.x, self.y, self.val, neighbors

    def get_val(self):
        return self.val, self.x, self.y

    def get_coords(self):
        return self.x, self.y

    def add_neighbors(self, grid, cols, rows):
        x = self.x
        y = self.y
        if x < cols - 1:
            self.neighbors.append(grid[x + 1][y])
        if x > 0:
            self.neighbors.append(grid[x - 1][y])
        if y < rows - 1:
            self.neighbors.append(grid[x][y + 1])
        if y > 0:
            self.neighbors.append(grid[x][y - 1])
