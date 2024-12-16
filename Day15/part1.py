# Warehouse Woes

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def put_output(filename, output):
    file = open(filename, "a")
    file.write(output)

def clear_output(filename):
    file = open(filename, "w")
    file.write("")

def output_grid(grid):
    filename = "Day15/output.txt"
    clear_output(filename)
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            put_output(filename, grid[i][j])
        put_output(filename, "\n")

def generate_grid(input):
    grid = []
    for i in range(0, len(input)):
        row = []
        for j in range(0, len(input[0])):
            row.append(input[i][j])
        grid.append(row)

    return grid

def get_start(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "@":
                return (i, j) # Start found
    return (-1, -1) # There's no start

def move_boxes(grid, direction, current_box_position):
    r = current_box_position[0]
    c = current_box_position[1]
    if direction == "^":
        # Go up
        new_box_position = (r - 1, c)
    elif direction == ">":
        # Go right
        new_box_position = (r, c + 1)
    elif direction == "v":
        # Go down
        new_box_position = (r + 1, c)
    elif direction == "<":
        # Move left
        new_box_position = (r, c - 1)

    # Update grid accordingly
    new_r = new_box_position[0]
    new_c = new_box_position[1]

    # Assume the box does move
    success = True

    if grid[new_r][new_c] == ".":
        # Box moves into empty space
        grid[new_r][new_c] = "O"
    elif grid[new_r][new_c] == "#":
        # Box moves into a wall, no change in position
        success = False
    elif grid[new_r][new_c] == "O":
        # Box tries to move one or more boxes
        success = move_boxes(grid, direction, new_box_position)
        if success:
            # Boxes were moved
            grid[new_r][new_c] = "O"
        # Otherwise, no boxes were moved
    return success

def process_moves(grid, moves):
    current_position = get_start(grid)

    for i in range(0, len(moves)):
        direction = moves[i]

        # Get new robot position based on move
        r = current_position[0]
        c = current_position[1]
        if direction == "^":
            # Go up
            new_position = (r - 1, c)
        elif direction == ">":
            # Go right
            new_position = (r, c + 1)
        elif direction == "v":
            # Go down
            new_position = (r + 1, c)
        elif direction == "<":
            # Move left
            new_position = (r, c - 1)

        # Update grid accordingly
        new_r = new_position[0]
        new_c = new_position[1]
        if grid[new_r][new_c] == ".":
            # Bot moves into empty space
            grid[new_r][new_c] = "@"
            grid[r][c] = "."
            current_position = new_position
        elif grid[new_r][new_c] == "#":
            # Bot moves into a wall, no change in position
            continue
        elif grid[new_r][new_c] == "O":
            # Bot tries to move one or more boxes
            success = move_boxes(grid, direction, new_position)
            if success:
                # Boxes were moved
                grid[new_r][new_c] = "@"
                grid[r][c] = "."
                current_position = new_position
            # Otherwise, neither the robot nor the boxes move

def get_boxes(grid):
    boxes = []
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "O":
                boxes.append((i, j))

    return boxes

def calculate_coord_sum(boxes):
    sum = 0
    for b in boxes:
        sum += 100 * b[0] + b[1]

    return sum

def main():
    input = get_input("Day15/input.txt").split("\n\n")
    grid_input = input[0].split("\n")
    moves = "".join(input[1].split("\n"))

    # Generate grid
    grid = generate_grid(grid_input)

    # Move the robot and the boxes
    process_moves(grid, moves)
    output_grid(grid)

    # Calculate sum of box coordinates
    boxes = get_boxes(grid)
    result = calculate_coord_sum(boxes)

    print(result)    

# Run program
main()