from PQ import PQ
import pygame

WIDTH = 800

VECTOR_X = [1, 0, -1, 0]
VECTOR_Y = [0, 1, 0, -1]

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualizer")

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

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        row = []
        for j in range(rows):
            row.append(Node(i, j, gap, rows))
        grid.append(row)
    return grid
    

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap), 1)
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width), 1)

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def BFS(draw, start, end):
    queue = []
    visited = []
    previous = {}
    queue.append(start)
    previous[start] = None
    visited.append(start)
    while len(queue) > 0:
        current = queue.pop(0)
        if current == end:
            while current != None:
                if current != start and current != end:
                    current.set_path()
                current = previous[current]
                draw()
            return True
        for neighbour in current.neighbours:
            if neighbour.is_wall() == False and neighbour not in visited:
                queue.append(neighbour)
                visited.append(neighbour)
                previous[neighbour] = current
                if neighbour != end:
                    neighbour.set_closed()
        draw()
    return False

def dijkstra(draw, grid, start, end):
    pq = PQ()
    distances = {}
    previous = {}
    infinity = float("inf")
    for row in grid:
        for node in row:
            if node == start:
                pq.enqueue(node, 0)
                distances[node] = 0
            else:
                pq.enqueue(node, infinity)
                distances[node] = infinity
            previous[node] = None

    while len(pq.values) > 0:
        minDistVertex = pq.dequeue()
        if minDistVertex == end:
            current = minDistVertex
            while current != None:
                if current != start and current != end:
                    current.set_path()
                current = previous[current]
                draw()
            return True
        for neighbour in minDistVertex.neighbours:
            if not neighbour.is_wall():
                nextNeighbourDist = distances[minDistVertex] + 1
                if neighbour != start and neighbour != end:
                    neighbour.set_visited()
                if(nextNeighbourDist < distances[neighbour]):
                    distances[neighbour] = nextNeighbourDist
                    previous[neighbour] = minDistVertex
                    pq.enqueue(neighbour, nextNeighbourDist)
                    if neighbour != start and neighbour != end:
                        neighbour.set_closed()
        draw()

    return False

def reset_algo(grid):
    for row in grid:
        for node in row:
            if not (node.is_wall() or node.is_start() or node.is_end()):
                node.reset()
    return grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows

    x, y = pos

    row = x // gap
    col = y // gap

    return row, col

def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started: continue
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if start is None and node != start:
                    start = node
                    node.set_start()
                elif end is None and node != start:
                    end = node
                    node.set_end()
                else:
                    if not (node.is_start() or node.is_end()):
                        node.set_wall()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if node.is_start():
                    start = None
                elif node.is_end():
                    end = None
                node.reset()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbours(ROWS, grid)
                    done = BFS(lambda: draw(win, grid, ROWS, width), start, end)
                    if done: started = False
                elif event.key == pygame.K_d and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbours(ROWS, grid)
                    done = dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    if done: started = False
                elif event.key == pygame.K_r:
                    grid = reset_algo(grid)
                    continue
    pygame.quit()

main(WIN, WIDTH)