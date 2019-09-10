import sys
import pygame
from node import Node

WIDTH = 60
HEIGHT = 60


# LEFT CLICK -> DRAW START NODE : 1
# SHIFT CLICK -> DRAW END NODE : 2
# CTRL CLICK -> DRAW WALL : 3
# press SPACE to reset everything

# Hit enter to start algorithm


class Pathfinder:
    colors = {
        1: (255, 0, 0),  # START NODE
        2: (0, 0, 255),  # END NODE
        3: (100, 100, 100),  # WALL
        4: (0, 255, 0)  # PATH
    }

    def __init__(self, width, height):
        pygame.init()
        self.white = 255, 255, 255
        self.scl = 20
        self.width = width
        self.height = height
        self.cols = self.width // self.scl
        self.rows = self.height // self.scl
        self.screen = pygame.display.set_mode((width, height))
        self.node_grid = [[Node(j, i, 0) for i in range(self.rows)] for j in range(self.cols)]
        self.start_node = False
        self.end_node = False
        self.start = None
        self.end = None
        self.open_set = []
        self.closed_set = []

    def reset(self):
        self.__init__(self.width, self.height)

    def draw_grid(self):
        black = 0, 0, 0
        for col in range(self.cols):
            var = (col * self.scl) - 1
            pygame.draw.line(self.screen, black, (var, 0), (var, self.height), 1)

        for row in range(self.rows):
            var = (row * self.scl) - 1
            pygame.draw.line(self.screen, black, (0, var), (self.width, var), 1)

    def set_nodes(self):
        # DRAW WALL
        if pygame.key.get_pressed()[pygame.K_LSHIFT] & pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            x = int(x // self.scl)
            y = int(y // self.scl)
            if self.get_cell(x, y) == 1:
                self.start_node = False
                self.start = None
            elif self.get_cell(x, y) == 2:
                self.end_node = False
                self.end = None
            self.set_cell(x, y, 3)
        # DELETE WALL
        elif pygame.key.get_pressed()[pygame.K_LCTRL] & pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            x = int(x // self.scl)
            y = int(y // self.scl)
            if self.get_cell(x, y) == 1:
                self.start_node = False
                self.start = None
            elif self.get_cell(x, y) == 2:
                self.end_node = False
                self.end = None
            self.set_cell(x, y, 0)
        else:
            # TODO: check if start or end node already exists
            if pygame.mouse.get_pressed()[0] and not self.start_node:
                x, y = pygame.mouse.get_pos()
                x = int(x // self.scl)
                y = int(y // self.scl)
                if self.get_cell(x, y) == 2:
                    self.end_node = False
                    self.end = None
                self.set_cell(x, y, 1)
                self.start_node = True
                self.start = Node(x, y, 1)
                # for node in self.node_grid:
                #    for n in node:
                #        print(n.__str__())

            elif pygame.mouse.get_pressed()[2] and not self.end_node:
                x, y = pygame.mouse.get_pos()
                x = int(x // self.scl)
                y = int(y // self.scl)
                if self.get_cell(x, y) == 1:
                    self.start_node = False
                    self.start = None
                self.set_cell(x, y, 2)
                self.end_node = True
                self.end = Node(x, y, 2)

    def draw_nodes(self):
        for c in range(self.cols):
            for r in range(self.rows):
                if self.node_grid[c][r].val in (1, 2, 3):
                    pygame.draw.rect(self.screen, self.colors[self.get_cell(c, r)],
                                     (c * self.scl, r * self.scl, self.scl, self.scl))

    def set_cell(self, x, y, val):
        #self.grid[x][y] = val
        self.node_grid[x][y].val = val

    def get_cell(self, x, y):
        return self.node_grid[x][y].val

    # check if start node exists
    def check_open(self, node):
        if node.val == 1 and len(self.open_set) == 0:
            self.open_set.append(node)
        elif node.val == 1 and len(self.open_set) > 0:
            self.open_set = []
            self.open_set.append(node)
        elif not self.start_node:
            self.open_set = []

    # Fill the grid with Node objects
    def create_node_grid(self):
        for c in range(self.cols):
            for r in range(self.rows):
                n = Node(r, c, 0)
                self.node_grid[c][r] = n
                self.check_open(n)

    # Add the neighbors to each node
    def add_neighbors(self):
        for c in range(self.cols):
            for r in range(self.rows):
                self.node_grid[c][r].add_neighbors(self.node_grid, self.cols, self.rows)

    def a_star(self):
        f = 0
        best = 0
        if len(self.open_set) > 0:
            for i in range(len(self.open_set)):
                if self.open_set[best].f > self.open_set[i].f:
                    best = i
                    f = self.open_set[i].f

            current_node = self.open_set[best]

            if self.open_set[best].get_coords == self.end.get_coords():
                print("DONE!")

            del self.open_set[best]
            self.closed_set.append(current_node)

            neighbors = current_node.neighbors

            for node in neighbors:
                if node in self.closed_set:
                    pass
                else:
                    temp_g = current_node.g + 1
                    if node in self.open_set:
                        if temp_g < node.g:
                            node.g = temp_g

        else:
            pass

    def run(self):
        self.create_node_grid()
        self.add_neighbors()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset()

            self.screen.fill(self.white)
            self.draw_grid()
            self.set_nodes()
            self.draw_nodes()
            pygame.display.flip()


if __name__ == "__main__":
    d = Pathfinder(WIDTH, HEIGHT)
    d.run()
