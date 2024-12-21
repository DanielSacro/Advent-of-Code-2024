# RAM Run
import heapq

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def put_output(filename, output):
    file = open(filename, "a")
    file.write(output)

def clear_output(filename):
    file = open(filename, "w")
    file.write("")

def generate_grid(input):
    grid = []
    for i in range(0, len(input)):
        row = []
        for j in range(0, len(input[0])):
            row.append(input[i][j])
        grid.append(row)
    return grid

def output_solution(grid): #, solution_path):
    # for node in solution_path:
    #     r = node.row
    #     c = node.col
    #     grid[r][c] = "O"

    filename = "Day20/output.txt"
    clear_output(filename)
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            put_output(filename, grid[i][j])
        put_output(filename, "\n")

# Implemented with help from university course - CMPUT 366
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.cost = 0
    
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
    child1 = Node(row - 1, col)
    if is_valid(grid, child1):
        children.append(child1)

    # Bottom
    child2 = Node(row + 1, col)
    if is_valid(grid, child2):
        children.append(child2)

    # Left
    child3 = Node(row, col - 1)
    if is_valid(grid, child3):
        children.append(child3)

    # Right
    child4 = Node(row, col + 1)
    if is_valid(grid, child4):
        children.append(child4)

    for c in children:
        c.cost = cost + 1

    return children

def get_S_and_E(grid):
    start_found = False
    end_found = False
    start = (-1, -1)
    end = (-1, -1)

    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "S":
                start = (i, j)
                start_found = True
            elif grid[i][j] == "E":
                end = (i, j)
                end_found = True
            
            if start_found and end_found:
                return start, end
            
    return start, end

# Yet another dijkstra - copied from day 18
def dijkstra(grid):
    # Initialize start and end nodes
    start_coords, end_coords = get_S_and_E(grid)
    start = Node(start_coords[0], start_coords[1])
    end = Node(end_coords[0], end_coords[1])
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

    # No solution
    return end.cost

def main():
    input = get_input("Day20/input.txt").split("\n")
    grid = generate_grid(input)

    original_time = dijkstra(grid)

    # Find out how many cheating routes result saving 100 picoseconds via brute force
    # Could be optimized by:
        # Running dijkstra once and creating a dictionary to hold the times for each point on the track
        # Removing wall's one by one and checking to see if we end up at a point later in the track
        # Using the dictionary to compare times to see how much time was saved
    # Alg. above saves time since dijkstra doesn't have to reach the end
    # Dijkstra only needs to reach a single later point on the track, and compare the times of that point
    count = 0
    THRESHOLD = 100
    loop = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            # Change a wall to a track and see how it affects the time
            if grid[i][j] == "#":
                grid[i][j] = "."
                time = dijkstra(grid)
                if original_time - time >= THRESHOLD:
                    count += 1
                grid[i][j] = "#"
            loop += 1
            print(f"Progress: {round(loop/(len(grid) * len(grid[0])) * 100, 2)}%")

    print(count)

# Run program
main()