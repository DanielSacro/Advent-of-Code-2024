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
    for i in range(0, tot_rows):
        row = []
        for j in range(0, tot_cols):
            row.append(rows[i][j])
        grid.append(row)
    return grid

def is_in_bounds(r, c, tot_rows, tot_cols):
    return -1 < r and r < tot_rows and -1 < c and c < tot_cols

def change_direction(direction):
    if direction < 3:
        direction += 1
    else:
        direction = 0
    return direction

def traverse(grid):
    # Find starting point "^"
    tot_rows = len(grid)
    tot_cols = len(grid[0])
    start_found = False
    for i in range(0, tot_rows):
        for j in range(0, tot_cols):
            if grid[i][j] == "^":
                start = [i, j]
                start_found = True
                break
        if start_found:
            break
    
    # Traverse
    direction = 0 # 0 = up, 1 = right, 2 = down, 3 = left
    r = start[0]
    c = start[1]
    while True:
        # print(r, c, direction)
        if direction == 0:
            # Try to go up 1
            if not is_in_bounds(r - 1, c, tot_rows, tot_cols):
                grid[r][c] = "X"
                break
            elif grid[r - 1][c] == "#":
                direction = change_direction(direction)
            else:
                grid[r][c] = "X"
                r -= 1
        elif direction == 1:
            # Try to go right 1
            if not is_in_bounds(r, c + 1, tot_rows, tot_cols):
                grid[r][c] = "X"
                break
            elif grid[r][c + 1] == "#":
                direction = change_direction(direction)
            else:
                grid[r][c] = "X"
                c += 1
        elif direction == 2:
            # Try to go down 1
            if not is_in_bounds(r + 1, c, tot_rows, tot_cols):
                grid[r][c] = "X"
                break
            elif grid[r + 1][c] == "#":
                direction = change_direction(direction)
            else:
                grid[r][c] = "X"
                r += 1
        elif direction == 3:
            # Try to go left 1
            if not is_in_bounds(r, c - 1, tot_rows, tot_cols):
                grid[r][c] = "X"
                break
            elif grid[r][c - 1] == "#":
                direction = change_direction(direction)
            else:
                grid[r][c] = "X"
                c -= 1
    return grid

def count_X(grid):
    count = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "X":
                count += 1
    return count

def main():
    input = get_input("Day6/input.txt")

    # Create a grid representing the map
    grid = generate_grid(input)
    # output_grid(grid)

    # Traverse the map, leaving X on the visited spots
    soln_grid = traverse(grid)
    output_grid(soln_grid)

    # Count the Xs
    result = count_X(soln_grid)

    print(result)
        
# Run program
main()