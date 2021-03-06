import sys
from collections import defaultdict


class Heap:

    def __init__(self):
        self.data = []

    def insert(self, score, item):
        from heapq import heappush
        heappush(self.data, (score, item))

    def pop_min(self):
        from heapq import heappop
        score, item = self.data[0]
        heappop(self.data)
        return item

    def __bool__(self):
        return bool(self.data)


def parse_data(file_name):
    with open(file_name, 'r') as f:
        content = f.readlines()
    grid = []
    for line in content:
        row = []
        for cel in line.strip():
            row.append(int(cel))
        grid.append(row)
    return grid


def create_graph(grid):
    """ Create graph from from list of lists """
    maze = defaultdict(dict)
    x_size = len(grid)
    y_size = len(grid[0])
    for x in range(x_size):
        for y in range(y_size):
            maze[(x, y)] = neighbours(grid, x_size, y_size, x, y)
    return maze


def neighbours(grid, x_size, y_size, x, y):
    raw_neighbours = [
        (x - 1, y),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y),
    ]
    real_neighbours = {}
    for i in raw_neighbours:
        if i[0] < 0 or i[1] < 0:
            continue
        if i[0] >= x_size or i[1] >= y_size:
            continue
        real_neighbours[i] = grid[i[0]][i[1]]
    return real_neighbours


# PART 1 - Dijkstra algorithm
def part_one(grid, target_node):
    maze = create_graph(grid)
    start_node = (0, 0)
    unvisited_nodes = Heap()
    unvisited_nodes.insert(0, start_node)
    shortest_path = {}
    previous_nodes = {}

    max_value = sys.maxsize
    for node in maze.keys():
        shortest_path[node] = max_value
    # initialize the starting node value with 0
    shortest_path[start_node] = 0

    # visit all nodes
    while unvisited_nodes:
        current_min_node = unvisited_nodes.pop_min()

        # current node's neighbors and updating their distances
        neighbors = maze[current_min_node]
        for neighbor in neighbors:
            tentative_value = (
                shortest_path[current_min_node] +
                maze[current_min_node][neighbor]
                )
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # best path to the current node
                previous_nodes[neighbor] = current_min_node
                unvisited_nodes.insert(tentative_value, neighbor)

    return shortest_path[target_node]


# PART two - extending map
def part_two(grid, target_node):
    # extending grid 5x to the side
    wide_grid = []
    for line in grid:
        new_line = []
        for i in range(5):
            for j in line:
                x = j + i
                if x > 9:
                    new_line.append(x - 9)
                else:
                    new_line.append(x)
        wide_grid.append(new_line)
    # make grid 5x longer
    long_grid = []
    for i in range(5):
        for line in wide_grid:
            new_line = []
            for j in line:
                x = j + i
                if x > 9:
                    new_line.append(x - 9)
                else:
                    new_line.append(x)
            long_grid.append(new_line)

    total_risk = part_one(long_grid, target_node)
    return total_risk


def main(file_name):
    grid = parse_data(file_name)
    part_1 = part_one(grid, (99, 99))
    part_2 = part_two(grid, (499, 499))
    return part_1, part_2


if __name__ == '__main__':
    part_1, part_2 = main("15_input.txt")

    print(f"Part one: {part_1}")
    print(f"Part two: {part_2}")
