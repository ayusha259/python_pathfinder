from PQ import PQ

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

def DFS(draw, start, end):
    stack = []
    visited = []
    previous = {}
    stack.append(start)
    previous[start] = None
    visited.append(start)
    while len(stack) > 0:
        current = stack.pop()
        if current == end:
            while current != None:
                if current != start and current != end:
                    current.set_path()
                current = previous[current]
                draw()
            return True
        for neighbour in current.neighbours:
            if neighbour.is_wall() == False and neighbour not in visited:
                stack.append(neighbour)
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