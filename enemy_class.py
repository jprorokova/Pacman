import pygame
import random
import numpy as np
import time

from settings import *
vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.prev_path = []
        self.path = []
        self.target = None
        self.speed = 1

        self.colour_path = list(np.random.choice(range(40,256), size=3))

    def update(self):
        self.draw_path(BLACK)

        self.target = self.set_target()

        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1
        self.find_path(self.app.player.grid_pos)
        self.draw_path(self.colour_path)

    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_target(self):
        # if self.personality == "speedy" or self.personality == "slow":
        #     return self.app.player.grid_pos
        # else:
        if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
            return vec(1, 1)
        if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] < ROWS//2:
            return vec(1, ROWS-2)
        if self.app.player.grid_pos[0] < COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
            return vec(COLS-2, 1)
        else:
            return vec(COLS-2, ROWS-2)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        self.direction = self.get_random_direction()

    def get_path_direction(self, target):
        next_cell = self.find_path(target)[1]
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_path(self, target):


        if self.app.player.alg == "DFS":
            start = time.time()


            self.path = self.app.alg.DFS([int(self.grid_pos[0]),int(self.grid_pos[1])],
                                    [int(target[0]),int(target[1])])
            stop = time.time()
            print("DFS")

        if self.app.player.alg == "BFS":
            start = time.time()
            self.path = self.app.alg.BFS([int(self.grid_pos[0]), int(self.grid_pos[1])],
                                    [int(target[0]), int(target[1])])
            stop = time.time()
            print("BFS")

        if self.app.player.alg == "uniform_cost_search":
            start = time.time()
            self.path = self.app.alg.uniform_cost_search([int(self.grid_pos[0]), int(self.grid_pos[1])],
                                         [int(target[0]), int(target[1])])
            stop = time.time()
            print("UCS")
        print(stop-start)

        # path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
        #                 int(target[0]), int(target[1])])



    def draw_path(self,COLOUR):
        # path = self.find_path(self.app.player.grid_pos)
        # if COLOUR == 'rand':
        #     COLOUR  = list(np.random.choice(range(25,256), size=3))
        # else:
        #     COLOUR = BLACK
        for xidx, yidx in self.path:
            pygame.draw.rect(self.app.background, COLOUR, (xidx * self.app.cell_width,  yidx* self.app.cell_height,
                                                        self.app.cell_width, self.app.cell_height))

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2 +
                   self.app.cell_height//2)

    def set_colour(self):
        if self.number == 0:
            return (43, 78, 203)
        if self.number == 1:
            return (197, 200, 27)
        if self.number == 2:
            return (189, 29, 29)
        if self.number == 3:
            return (215, 159, 33)






