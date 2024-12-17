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
            tile = input[i][j]
            if tile == "#" or tile == ".":
                row.append(tile)
                row.append(tile)
            elif tile == "O":
                row.append("[")
                row.append("]")
            elif tile == "@":
                row.append(tile)
                row.append(".")
        grid.append(row)

    return grid

def get_start(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "@":
                return (i, j) # Start found
    return (-1, -1) # There's no start

def move_boxes(grid, direction, current_box_position, box_half):
    if box_half == "[":
        left_half = current_box_position
        right_half = (current_box_position[0], current_box_position[1] + 1)
    elif box_half == "]":
        right_half = current_box_position
        left_half = (current_box_position[0], current_box_position[1] - 1)

    left_r = left_half[0]
    left_c = left_half[1]
    right_r = right_half[0]
    right_c = right_half[1]

    if direction == "^":
        # Go up
        new_left_half = (left_r - 1, left_c)
        new_right_half = (right_r - 1, right_c)
    elif direction == ">":
        # Go right
        new_left_half = (left_r, left_c + 1)
        new_right_half = (right_r, right_c + 1)
    elif direction == "v":
        # Go down
        new_left_half = (left_r + 1, left_c)
        new_right_half = (right_r + 1, right_c)
    elif direction == "<":
        # Move left
        new_left_half = (left_r, left_c - 1)
        new_right_half = (right_r, right_c - 1)

    # Update grid accordingly
    new_left_r = new_left_half[0]
    new_left_c = new_left_half[1]
    new_right_r = new_right_half[0]
    new_right_c = new_right_half[1]

    # Assume the box does move
    success = True

    # Handle all cases of box(es) moving
    if direction == "<":
        # Box moves left
        if grid[new_left_r][new_left_c] == ".":
            # Box moves left into empty space
            grid[new_left_r][new_left_c] = "["
            grid[new_right_r][new_right_c] = "]"
        elif grid[new_left_r][new_left_c] == "#":
            # Box moved into wall and doesn't move
            success = False
        elif grid[new_left_r][new_left_c] == "]":
            # Box tries to move one or more boxes left
            success = move_boxes(grid, direction, new_left_half, "]")
            if success:
                # Boxes were successfully moved
                grid[new_left_r][new_left_c] = "["
                grid[new_right_r][new_right_c] = "]"
            # Otherwise, no boxes could be moved
    elif direction == ">":
        # Box moves right
        if grid[new_right_r][new_right_c] == ".":
            # Empty space on right
            grid[new_left_r][new_left_c] = "["
            grid[new_right_r][new_right_c] = "]"
        elif grid[new_right_r][new_right_c] == "#":
            # Wall on right
            success = False
        elif grid[new_right_r][new_right_c] == "[":
            # More boxes on right
            success = move_boxes(grid, direction, new_right_half, "[")
            if success:
                grid[new_left_r][new_left_c] = "["
                grid[new_right_r][new_right_c] = "]"
    elif direction == "^" or direction == "v":
        # Box moves up
        if grid[new_left_r][new_left_c] == "." and grid[new_right_r][new_right_c] == ".":
            # Empty space above
            grid[new_left_r][new_left_c] = "["
            grid[new_right_r][new_right_c] = "]"
        elif grid[new_left_r][new_left_c] == "#" or grid[new_right_r][new_right_c] == "#":
            # Wall above
            success = False
        else:
            if grid[new_left_r][new_left_c] == "[" and grid[new_right_r][new_right_c] == "]":
                # One box directly above
                success = move_boxes(grid, direction, new_left_half, "[")
            else:
                # One or more boxes diagonally above
                # In the case there is only one box diagonally above, other side can be moved
                left_success = True
                right_success = True

                if grid[new_left_r][new_left_c] == "]":
                    # Have to move the top left box
                    left_success = move_boxes(grid, direction, new_left_half, "]")
                    if left_success:
                        grid[new_left_r][new_left_c - 1] = "."
                
                if grid[new_right_r][new_right_c] == "[":
                    # Have to move the top right box
                    right_success = move_boxes(grid, direction, new_right_half, "[")
                    if right_success:
                        grid[new_right_r][new_right_c + 1] = "."
                
                if left_success and right_success:
                    # Both sides of boxes could be moved
                    grid[new_left_r][new_left_c] = "["
                    grid[new_right_r][new_right_c] = "]"
                else:
                    # Otherwise, one side of the boxes couldn't be moved => reset.
                    success = False
            
    return success

def copy_grid(grid):
    new_grid = []
    for i in range(0, len(grid)):
        row = []
        for j in range(0, len(grid[0])):
            row.append(grid[i][j])
        new_grid.append(row)
    return new_grid

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
            if direction == "^" or direction == "v":
                # Have to update where one half of the box used to be to "."
                if grid[new_r][new_c] == "[":
                    # Pushed the left half
                    grid[new_r][new_c + 1] = "."
                elif grid[new_r][new_c] == "]":
                    grid[new_r][new_c - 1] = "."
            grid[new_r][new_c] = "@"
            grid[r][c] = "."
            current_position = new_position
        elif grid[new_r][new_c] == "#":
            # Bot moves into a wall, no change in position
            continue
        elif grid[new_r][new_c] == "[" or grid[new_r][new_c] == "]":
            # Bot tries to move one or more boxes
            original_grid = copy_grid(grid)
            success = move_boxes(grid, direction, new_position, grid[new_r][new_c])
            if success:
                # Boxes were moved
                if direction == "^" or direction == "v":
                    # Have to update where one half of the box used to be to "."
                    if grid[new_r][new_c] == "[":
                        # Pushed the left half
                        grid[new_r][new_c + 1] = "."
                    elif grid[new_r][new_c] == "]":
                        grid[new_r][new_c - 1] = "."
                grid[new_r][new_c] = "@"
                grid[r][c] = "."
                current_position = new_position
            elif not success:
                # Otherwise, neither the robot nor the boxes move
                # Reset grid in case that on side of boxes moved and another side didn't
                grid = original_grid
    return grid

def get_boxes(grid):
    boxes = []
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "[":
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
    grid = process_moves(grid, moves)
    output_grid(grid)

    # Calculate sum of box coordinates
    boxes = get_boxes(grid)
    result = calculate_coord_sum(boxes)

    print(result)    

# Run program
main()