import pygame

VECTOR_X = [1, 0, -1, 0]
VECTOR_Y = [0, 1, 0, -1]

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.color = WHITE
        self.neighbours = []
        self.total_rows = total_rows
    
    def get_position(self):
        return self.row, self.col
    
    def get_cords(self):
        return self.x, self.y
    
    def is_closed(self):
        return self.color == RED
    
    def is_visited(self):
        return self.color == GREEN
    
    def is_wall(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == PURPLE
    
    def reset(self):
        self.color = WHITE
    
    def set_closed(self):
        self.color = RED
    
    def set_visited(self):
        self.color = GREEN
    
    def set_wall(self):
        self.color = BLACK
    
    def set_start(self):
        self.color = ORANGE
    
    def set_end(self):
        self.color = PURPLE
    
    def set_path(self):
        self.color = YELLOW
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbours(self, rows, grid):
        for i in range(4):
            ncol = VECTOR_X[i] + self.col
            nrow = VECTOR_Y[i] + self.row

            if nrow >= 0 and nrow < rows and ncol >= 0 and ncol < rows:
                self.neighbours.append(grid[nrow][ncol])
    
    def __lt__(self, other):
        return False