# Claw Contraption

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def play(machine):
    # Parse input for numbers
    inputs = machine.split("\n")
    A_inputs = inputs[0].split(" ")[2:]
    B_inputs = inputs[1].split(" ")[2:]
    prize_inputs = inputs[2].split(" ")[1:]

    A_x = int(A_inputs[0][2:-1])
    A_y = int(A_inputs[1][2:])

    B_x = int(B_inputs[0][2:-1])
    B_y = int(B_inputs[1][2:])

    unit_change = 10000000000000
    X = int(prize_inputs[0][2:-1]) + unit_change
    Y = int(prize_inputs[1][2:]) + unit_change

    # Debug
    # print(A_x, A_y)
    # print(B_x, B_y)
    # print(X, Y)

    # Assumptions:
        # System of equations has 1 right answer
        # A and B are not duplicate buttons with different costs | Example: A_x != B_x
        # A and B always cause the crane to move in BOTH the x and y directions | Example: A_x != 0 and A_y != 0

    # Calculate times B needs to be pressed -> Derived using algebra
    B = (Y - A_y * X / A_x) / (B_y - B_x * A_y / A_x)
    B = round(B, 3) # Because some integers represented as X.0001 and not as X.0

    # Calculate times A needs to be pressed -> Derived using algebra
    A = (X - B * B_x) / A_x
    A = round(A, 3)

    if not A.is_integer() or not B.is_integer():
        print(A, B)
        return 0
    elif A < 0 or B < 0:
        # Can't press a button negative times
        return 0
    else:
        cost = 3 * A + B
        print(cost)
        return cost

def main():
    input = get_input("Day13/input.txt")
    machines = input.split("\n\n")

    total = 0
    for m in machines:
        print(m)
        tokens_used = play(m)
        print("\n")
        if tokens_used > 0:
            total += tokens_used
        
    result = total
    print(result)
        
# Run program
main()