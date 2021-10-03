from queue import PriorityQueue
import time
class Algs:
    def __init__(self, walls):
        self.grid = [[0 for x in range(28)] for x in range(30)]
        for cell in walls:
            if cell.x < 28 and cell.y < 30:
                self.grid[int(cell.y)][int(cell.x)] = 1

    def uniform_cost_search(self, start,goal):

        queue = PriorityQueue()
        queue.put((0, [start]))
        visited = []
        while not queue.empty():
            pair = queue.get()
            current = pair[1][-1]
            cost = pair[0]
            if current == goal:
                return pair[1]
            neighbours = [[int(current[0] + 1), int(current[1])],
                          [int(current[0] - 1), int(current[1])],
                          [int(current[0]), int(current[1] + 1)],
                          [int(current[0]), int(current[1] - 1)]]
            for neighbour in neighbours:
                if 0 <= neighbour[0] < len(self.grid[0]):
                    if 0 <= neighbour[1] < len(self.grid):
                        next_cell = [int(neighbour[0]), int(neighbour[1])]
                        if self.grid[int(next_cell[1])][next_cell[0]] != 1 and next_cell not in visited:
                            visited.append(next_cell)
                            temp = pair[1][:]
                            temp.append(next_cell)
                            queue.put((cost + self.cost_function(next_cell, goal), temp))

    def cost_function(self, point, end):
        return pow(point[0] - end[0], 2) + pow(point[1] - end[1], 2)
    def BFS(self, start, goal):
        queue = [(start, [start])]
        visited = []
        while queue:
            (current, path) = queue.pop(0)
            visited.append(current)
            neighbours = [[int(current[0] + 1), int(current[1])],
                          [int(current[0] - 1), int(current[1])],
                          [int(current[0]), int(current[1] + 1)],
                          [int(current[0]), int(current[1] - 1)]]
            for neighbour in neighbours:
                if 0 <= neighbour[0] < len(self.grid[0]):
                    if 0 <= neighbour[1] < len(self.grid):
                        next_cell = [int(neighbour[0]), int(neighbour[1])]
                        if self.grid[int(next_cell[1])][next_cell[0]] != 1:
                            if next_cell == goal:
                                return path + [goal]
                            else:
                                if next_cell not in visited:
                                    visited.append(next_cell)
                                    queue.append((next_cell, path + [next_cell]))

    def DFS(self, start, goal):
        stack = [(start, [start])]
        visited = []
        while stack:
            (current, path) = stack.pop()
            if current not in visited:
                if current == goal:
                    return path
                visited.append(current)
                neighbours = [[int(current[0] + 1), int(current[1])],
                              [int(current[0] - 1), int(current[1])],
                              [int(current[0]), int(current[1] + 1)],
                              [int(current[0]), int(current[1] - 1)]]
                for neighbour in neighbours:
                    if 0 <= neighbour[0] < len(self.grid[0]):
                        if 0 <= neighbour[1] < len(self.grid):
                            next_cell = [int(neighbour[0]), int(neighbour[1])]
                            if self.grid[int(next_cell[1])][next_cell[0]] != 1:
                                stack.append((next_cell, path + [next_cell]))

    def count_time(self,func):
        start = time.time()

        stop = time.time()
        return stop-start
