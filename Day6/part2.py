# Guard Gallivant

def get_input(filename):
    file = open(filename, "r")
    return file.read()

# For debugging
def put_output(filename, output):
    file = open(filename, "a")
    file.write(output)

def clear_output(filename):
    file = open(filename, "w")
    file.write("")

def output_grid(grid):
    output_file = "Day6/output.txt"
    clear_output(output_file)
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            put_output(output_file, grid[i][j])
        put_output(output_file, "\n")

def generate_grid(input):
    rows = input.split("\n")
    tot_rows = len(rows)
    tot_cols = len(rows[0])

    grid = []
    start = []
    for i in range(0, tot_rows):
        row = []
        for j in range(0, tot_cols):
            if rows[i][j] == "^":
                start.extend([i, j])
            row.append(rows[i][j])
        grid.append(row)
    return grid, start

def is_in_bounds(r, c, tot_rows, tot_cols):
    return -1 < r and r < tot_rows and -1 < c and c < tot_cols

def change_direction(direction):
    if direction < 3:
        direction += 1
    else:
        direction = 0
    return direction

def is_loop(grid, start):
    tot_rows = len(grid)
    tot_cols = len(grid[0])
    
    # Keep track of what nodes were visited
    seen = set()

    # Traverse
    direction = 0 # 0 = up, 1 = right, 2 = down, 3 = left
    r = start[0]
    c = start[1]
    while (r, c, direction) not in seen:
        # Loop not found yet, keep traversing
        if direction == 0:
            # Try to go up 1
            if not is_in_bounds(r - 1, c, tot_rows, tot_cols):
                # Out of bounds, not a loop
                return False
            elif grid[r - 1][c] == "#":
                direction = change_direction(direction)
            else:
                # Remember the last node we were at
                seen.add((r, c, direction))
                r -= 1
        elif direction == 1:
            # Try to go right 1
            if not is_in_bounds(r, c + 1, tot_rows, tot_cols):
                return False
            elif grid[r][c + 1] == "#":
                direction = change_direction(direction)
            else:
                seen.add((r, c, direction))
                c += 1
        elif direction == 2:
            # Try to go down 1
            if not is_in_bounds(r + 1, c, tot_rows, tot_cols):
                return False
            elif grid[r + 1][c] == "#":
                direction = change_direction(direction)
            else:
                seen.add((r, c, direction))
                r += 1
        elif direction == 3:
            # Try to go left 1
            if not is_in_bounds(r, c - 1, tot_rows, tot_cols):
                return False
            elif grid[r][c - 1] == "#":
                direction = change_direction(direction)
            else:
                seen.add((r, c, direction))
                c -= 1
    # While loop breaks if a guard's loop was found
    return True

def find_loops(grid, start):
    # Naive Brute Force Alg. -> Slow, but not super slow because input isn't super big

    # Find a spot to place a new obstacle
    count = 0
    for r in range(0, len(grid)):
        for c in range(0, len(grid[0])):
            # Check if we can place a new obstacle here
            if grid[r][c] ==  "^" or grid[r][c] == "#":
                # Only place on "".""
                continue
            
            # Place new obstacle
            grid[r][c] = "#"

            # Check if it causes a loop
            if is_loop(grid, start):
                # Keep track of how many loops are created
                count += 1
            
            # Remove previous obstacle
            grid[r][c] = "."
    return count

def main():
    input = get_input("Day6/input.txt")

    # Create a grid representing the map
    grid, start = generate_grid(input)
    # output_grid(grid)

    # Find and count loops
    result = find_loops(grid, start)

    print(result)
        
# Run program
main()