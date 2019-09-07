# TODO: f(x) = g(x) + h(x)


class Node:
    """
    Node values:
        1: start
        2: end
        3: wall
        0: empty
    """

    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val
        self.f = 0
        self.g = 0
        self.h = 0

    def get_val(self):
        return self.val, self.x, self.y
