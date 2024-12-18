# RAM Run
import heapq
MAX_SIDE_LENGTH = 71
TOT_BYTES_FALLEN = 1024

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def put_output(filename, output):
    file = open(filename, "a")
    file.write(output)

def clear_output(filename):
    file = open(filename, "w")
    file.write("")

def output_solution(grid, solution_path):
    for node in solution_path:
        r = node.row
        c = node.col
        grid[r][c] = "O"

    filename = "Day18/output.txt"
    clear_output(filename)
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            put_output(filename, grid[i][j])
        put_output(filename, "\n")

def generate_grid():
    grid = []
    for i in range(0, MAX_SIDE_LENGTH):
        row = []
        for j in range(0, MAX_SIDE_LENGTH):
            row.append(".")
        grid.append(row)
    return grid

def drop_bytes(grid, bytes):
    for i in range(0, TOT_BYTES_FALLEN):
        coords = bytes[i].split(",")
        row = int(coords[1])
        col = int(coords[0])

        grid[row][col] = "#"

# Implemented with help from university course - CMPUT 366
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.cost = 0
        self.prev = None
    
    # For min heap
    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

def is_valid(grid, current):
    return -1 < current.row and current.row < len(grid) and -1 < current.col and current.col < len(grid[0]) and grid[current.row][current.col] != "#"

def get_children(grid, current):
    children = []
    row = current.row
    col = current.col
    cost = current.cost
    
    # Top
    child1 = Node(current.row - 1, current.col)
    if is_valid(grid, child1):
        children.append(child1)

    # Bottom
    child2 = Node(current.row + 1, current.col)
    if is_valid(grid, child2):
        children.append(child2)

    # Left
    child3 = Node(current.row, current.col - 1)
    if is_valid(grid, child3):
        children.append(child3)

    # Right
    child4 = Node(current.row, current.col + 1)
    if is_valid(grid, child4):
        children.append(child4)

    for c in children:
        c.prev = current
        c.cost = cost + 1

    return children

# Implemented with help from university course - CMPUT 366
def dijkstra(grid):
    # Initialize start and end nodes
    start = Node(0, 0)
    end = Node(MAX_SIDE_LENGTH - 1, MAX_SIDE_LENGTH - 1)
    end.cost = -1 # Default value for when no solution is found

    # Initialize OPEN and CLOSED lists
    open = []
    closed = {}
    closed[(start.row, start.col)] = start
    heapq.heappush(open, start)

    while len(open) != 0:
        current = heapq.heappop(open)
        # print(current.row, current.col, current.cost)

        # Check if we reached the end
        if current == end:
            end = current
            break

        # Didn't reach the end, generate children
        children = get_children(grid, current)
        for c in children:
            hash = (c.row, c.col)
            if hash not in closed:
                # New child
                closed[hash] = c
                heapq.heappush(open, c)
            elif hash in closed and c.cost < closed[hash].cost:
                # Child seen before, but its cost is cheaper now
                closed[hash].cost = c.cost # Should update same instance of child in both open and closed lists
                closed[hash].prev = c.prev
                heapq.heapify(open)

    solution_path = []
    node = end
    while True:
        try:
            solution_path.append(node)
            node = node.prev
        except:
            solution_path.pop()
            break

    # No solution
    return end.cost, solution_path

def main():
    input = get_input("Day18/input.txt")
    bytes = input.split("\n")

    grid = generate_grid()

    drop_bytes(grid, bytes)

    steps, path = dijkstra(grid)
    output_solution(grid, path)

    print(steps)

# Run program
main()