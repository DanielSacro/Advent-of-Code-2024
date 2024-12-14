# Restroom Redoubt

from queue import Queue

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def get_new_position(robot, time):
    # Parse input for starting positions and velocities
    inputs = robot.split(" ")
    p = inputs[0][2:].split(",")
    v = inputs[1][2:].split(",")

    current_position = (int(p[0]), int(p[1]))
    velocity = (int(v[0]), int(v[1]))

    # print(current_position, velocity) # Debug

    # Move robot as if bathroom space was infinite
    x_position = current_position[0] + velocity[0] * time
    y_position = current_position[1] + velocity[1] * time

    # Correct robot's position by teleporting it to the right position (edge wrapping)
    bathroom_width = 101
    bathroom_height = 103
    x_position = x_position % bathroom_width
    y_position = y_position % bathroom_height

    new_position = (x_position, y_position)
    return new_position

def get_quadrant(position):
    x = position[0]
    y = position[1]

    quadrant = -1
    x_mid = (101 - 1) / 2
    y_mid = (103 - 1) / 2
    if x < x_mid and y < y_mid:
        quadrant = 0
    elif x > x_mid and y < y_mid:
        quadrant = 1
    elif x < x_mid and y > y_mid:
        quadrant = 2
    elif x > x_mid and y > y_mid:
        quadrant = 3

    return quadrant

def put_output(filename, output):
    file = open(filename, "a")
    file.write(output)

def print_position(positions):
    # Generate grid
    grid = []
    grid_width = 101
    grid_height = 103
    for r in range(0, grid_height):
        row = []
        for c in range(0, grid_width):
            row.append(".")
        grid.append(row)
    
    for p in positions:
        r = p[1]
        c = p[0]
        if grid[r][c] == ".":
            grid[r][c] = 1
        else:
            grid[r][c] += 1


    output_file = "Day14/output.txt"
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            put_output(output_file, str(grid[i][j]))
        put_output(output_file, "\n")
    put_output(output_file, "\n")

def get_neighbors(position):
    neighbors = []
    x = position[0]
    y = position[1]

    neighbors.append((x - 1, y))
    neighbors.append((x + 1, y))
    neighbors.append((x, y - 1))
    neighbors.append((x, y + 1))
    return neighbors

# Hint from reddit - rather than manually sifting through thousands of images, find a configuration where bots are abnormally clustered together
def find_largest_region(positions):
    # Inspiration from day 12's region counting
    visited = set()
    search_space = Queue()

    region_sizes = []
    for p in positions:
        search_space.put(p)

        # Ignore robots already visited
        if p in visited:
            continue

        count = 0
        while not search_space.empty():
            robot = search_space.get()
            # print(robot)
            # Again, ignore robots already visited
            if robot in visited:
                continue
            elif robot not in positions:
                continue
            else:
                visited.add(robot)
                count += 1

            neighbors = get_neighbors(robot)
            for n in neighbors:
                if n in visited:
                    continue
                if n in positions:
                    search_space.put(n)
        region_sizes.append(count)
    return max(region_sizes)

def main():
    input = get_input("Day14/input.txt")
    robots = input.split("\n")
    
    for time in range(0, 20000):
        print(f"Simulating time t={time}s")
        positions = []
        for r in robots:
            p = get_new_position(r, time)
            positions.append(p)
        size = find_largest_region(positions)

        if size > 16: # Magic number that found the christmas tree and ignored random clusters of robots
            print(f"Potential Christmas Tree Found, size={size}")
            put_output("Day14/output.txt", f"Time t={time}s\n")
            print_position(positions)
            print("Potential Christmas Tree printed to output.txt")
            break
    print("Simulation complete.")
        
# Run program
main()