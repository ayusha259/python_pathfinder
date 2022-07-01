from algos import BFS, DFS, dijkstra
from Node import Node, GREY, WHITE
import pygame

WIDTH = 800


WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualizer")



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
                elif event.key == pygame.K_p and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbours(ROWS, grid)
                    done = DFS(lambda: draw(win, grid, ROWS, width), start, end)
                    if done: started = False
                elif event.key == pygame.K_r:
                    grid = reset_algo(grid)
                    continue
    pygame.quit()

main(WIN, WIDTH)