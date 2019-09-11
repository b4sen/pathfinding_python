import sys
import pygame
from node import Node
import math

WIDTH = 600
HEIGHT = 600


# LEFT CLICK -> DRAW START NODE : 1
# SHIFT CLICK -> DRAW END NODE : 2
# CTRL CLICK -> DRAW WALL : 3
# press SPACE to reset everything

# Hit enter to start algorithm


# TODO: check if start node is not overwritten,
# if it is, remove the previous from the open_set and add the new one


class Pathfinder:
    colors = {
        1: (255, 0, 0),  # START NODE
        2: (0, 0, 255),  # END NODE
        3: (100, 100, 100),  # WALL
        4: (0, 255, 0),  # VISITED
        5: (0, 255, 255)  # PATH
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
        self.path = []
        self.done = False

    def reset(self):
        self.__init__(self.width, self.height)
        self.add_neighbors()

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
                self.start = self.node_grid[x][y]
                self.open_set.append(self.node_grid[x][y])  # TEMPORARY SOLUTION FOR check_open(node)
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
                self.end = self.node_grid[x][y]

    def draw_nodes(self):
        for c in range(self.cols):
            for r in range(self.rows):
                if self.node_grid[c][r].val in self.colors:
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

    # Add the neighbors to each node
    def add_neighbors(self):
        for c in range(self.cols):
            for r in range(self.rows):
                self.node_grid[c][r].add_neighbors(self.node_grid, self.cols, self.rows)

    def calculate_distance(self, x, y):
        return(math.sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2)))

    # the algorithm itself!
    # TODO: fix the bug!! it's not working
    def a_star(self):
        best = self.open_set[0]
        if len(self.open_set) > 0:
            for node in self.open_set:
                if best.f > node.f:
                    best = node

            current_node = best
            # Find the path
            if current_node.get_coords() == self.end.get_coords():
                temp_node = current_node
                while temp_node.came_from is not self.start:
                    self.path.append(temp_node.came_from)
                    temp_node = temp_node.came_from
                for n in self.path:
                    n.val = 5
                # print("DONE!")
                return

            self.open_set.remove(best)
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
                        node.g = temp_g
                        if node.val != 2:
                            node.val = 4
                        self.open_set.append(node)
                    node.h = self.calculate_distance(node.get_coords(), self.end.get_coords())
                    node.f = node.g + node.h
                    node.came_from = current_node

        else:
            pass

    def run(self):
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
            if self.start_node and self.end_node:
                self.a_star()
            pygame.display.flip()


if __name__ == "__main__":
    d = Pathfinder(WIDTH, HEIGHT)
    d.run()
