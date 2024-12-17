# Reindeer Maze
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

def output_solution(grid, best_tiles):
    for tile in best_tiles:
        r = tile[0]
        c = tile[1]
        grid[r][c] = "."
        # print(r, c, node.cost)

    filename = "Day16/output.txt"
    clear_output(filename)
    for i in range(0, len(grid)):
        row = ""
        for j in range(0, len(grid[0])):
            row += grid[i][j]
        put_output(filename, row + "\n")

def generate_grid(input):
    grid = []
    for i in range(0, len(input)):
        row = []
        for j in range(0, len(input[0])):
            if input[i][j] == ".":
                row.append(" ")
            else:
                row.append(input[i][j])
        grid.append(row)
    return grid            

# Implemented with help from university course - CMPUT 366
class Node:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.cost = 0
        self.prev = None
    
    # For min heap
    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

def get_path_ends(grid):
    start = (-1, -1)
    end = (-1, -1)
    start_found = False
    end_found = False
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "S":
                start = (i, j)
                start_found = True
            elif grid[i][j] == "E":
                end = (i, j)
                end_found = True
            elif start_found and end_found:
                # Start and end found
                return start, end
    # Start and end not found
    return start, end

def get_children(grid, current):
    children = []
    
    # Child based 90 degree turn clockwise -> 0 = North, 1 = East, 2 = South, 3 = West
    child1 = Node(current.row, current.col, 0)
    if current.direction < 3:
        child1.direction = current.direction + 1
    else:
        child1.direction = 0
    child1.cost = current.cost + 1000
    child1.prev = current
    children.append(child1)

    # Child based on 90 degree turn counterclockwise
    child2 = Node(current.row, current.col, 0)
    if current.direction > 0:
        child2.direction = current.direction - 1
    else:
        child2.direction = 3
    child2.cost = current.cost + 1000
    child2.prev = current
    children.append(child2)

    # Child based on moving forward one square in the direction current is facing
    if current.direction == 0:
        # North
        new_position = (current.row - 1, current.col)
    elif current.direction == 1:
        # East
        new_position = (current.row, current.col + 1)        
    elif current.direction == 2:
        # South
        new_position = (current.row + 1, current.col)
    elif current.direction == 3:
        # West
        new_position = (current.row, current.col - 1)
    
    if grid[new_position[0]][new_position[1]] != "#":
        child3 = Node(new_position[0], new_position[1], current.direction)
        child3.cost = current.cost + 1
        child3.prev = current
        children.append(child3)

    return children

# Implemented with help from university course - CMPUT 366
def dijkstra(grid):
    # Run dijkstra once to find the best path

    # Initialize start and end nodes
    start_coords, end_coords = get_path_ends(grid)
    start = Node(start_coords[0], start_coords[1], 1) # 1 = East
    end = Node(end_coords[0], end_coords[1], 0) # Direction is ignored when checking if we reached the end
    end.cost = -1 # Default value for when no solution is found

    # Initialize OPEN and CLOSED lists
    open = []
    closed = {}
    closed[(start.row, start.col, start.direction)] = start
    heapq.heappush(open, start)

    while len(open) != 0:
        current = heapq.heappop(open)
        # print(current.row, current.col, current.direction, current.cost)

        # Check if we reached the end
        if current == end:
            end = current
            break

        # Didn't reach the end, generate children
        children = get_children(grid, current)
        for c in children:
            hash = (c.row, c.col, c.direction)
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

    return end.cost, solution_path

def find_alternatives(grid, solution_path):    
    # Run Dijkstra again, remembering the best path
    # Any time you reach a node in the best path with the same cost as the node, it's another best path
    best_tiles = set()
    for node in solution_path:
        tile = (node.row, node.col, node.direction, node.cost)
        best_tiles.add(tile)

    # Initialize start and end nodes
    start_coords, end_coords = get_path_ends(grid)
    start = Node(start_coords[0], start_coords[1], 1) # 1 = East
    end = Node(end_coords[0], end_coords[1], 0) # Direction is ignored when checking if we reached the end
    end.cost = -1 # Default value for when no solution is found

    # Initialize OPEN and CLOSED lists
    open = []
    closed = {}
    closed[(start.row, start.col, start.direction)] = start
    heapq.heappush(open, start)
    print(best_tiles)
    while len(open) != 0:
        current = heapq.heappop(open)
        tile = (current.row, current.col, current.direction, current.cost)
        print(tile)

        # Check if we reached the solution path
        if tile in best_tiles:
            node = current
            while True:
                try:
                    best_tiles.add(tile)
                    node = node.prev
                    tile = (node.row, node.col, node.direction, node.cost)
                except:
                    break

        # Didn't reach a solution path, generate children
        children = get_children(grid, current)
        for c in children:
            hash = (c.row, c.col, c.direction)
            if hash not in closed:
                # New child
                closed[hash] = c
                heapq.heappush(open, c)
    print(best_tiles)
    return best_tiles


def main():
    input = get_input("Day16/input.txt").split("\n")
    grid = generate_grid(input)

    score, solution_path = dijkstra(grid)
    solution_tiles = find_alternatives(grid, solution_path)

    # output_solution(grid, solution_path)
    output_solution(grid, solution_tiles)

    print(score)    

# Run program
main()