# Restroom Redoubt

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def get_new_position(robot):
    # Parse input for starting positions and velocities
    inputs = robot.split(" ")
    p = inputs[0][2:].split(",")
    v = inputs[1][2:].split(",")

    current_position = (int(p[0]), int(p[1]))
    velocity = (int(v[0]), int(v[1]))

    # print(current_position, velocity) # Debug

    # Move robot as if bathroom space was infinite
    time = 100 
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

def main():
    input = get_input("Day14/input.txt")
    robots = input.split("\n")
    
    quadrants = [0, 0, 0, 0]
    for r in robots:
        p = get_new_position(r)
        q = get_quadrant(p)
        if q > -1:
            quadrants[q] += 1
        print(p, q)
    print(quadrants)
    safety_factor = 1
    for q in quadrants:
        safety_factor *= q

    result = safety_factor
    print(result)
        
# Run program
main()