# Bridge Repair
from queue import Queue

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def get_target(e):
    return int(e.split(" ")[0][:-1])

def calc(numbers, operators, target):
    # Calculate equation from left to right, not following BEDMAS
    result = int(numbers[0])
    for i in range(0, len(operators)):
        curr_num = int(numbers[i + 1])
        if result > target:
            break
        elif operators[i] == "*":
            result *= curr_num
        elif operators[i] == "+":
            result += curr_num
        elif operators[i] == "|":
            result = int(str(result) + str(curr_num))

    return result

def is_solvable(e):
    numbers = e.split(" ")[1:]
    target = get_target(e)

    # Try all +s first
    starting_operators = ""
    for i in range(0, len(numbers) - 1):
        starting_operators += "+"
    
    # Initialize search space
    search_space = Queue()
    search_space.put(starting_operators)

    # Avoid redundant searches
    checked = set()

    # Start search using BFS (with a queue)
    while not search_space.empty():
        operators = search_space.get()

        # Ignore operators already checked
        if operators in checked:
            continue

        if target == calc(numbers, operators, target):
            # Target found
            return True
        else:
            # Target not found; Keep searching while avoiding redundant searches
            checked.add(operators)

        # Generate new nodes to search using the current operators (by converting +s into *s)
        children = []
        for i in range(0, len(operators)):
            new_operators = [*operators] # Convert operators from string to list

            # Generate a new child node, where a + is changed to a *
            if new_operators[i] == "+":
                new_operators[i] = "*"
                new_operators = "".join(new_operators) # Convert operators from list to string
                
                # Don't bother adding the child if it's already been searched
                if new_operators not in checked:
                    search_space.put(new_operators)
                    children.append(new_operators)
        
        # Generate more nodes to search using the current operators and children nodes (by converting + or * into |)
        for child in children:
            for i in range(0, len(operators)):
                new_child = [*child]
                if new_child[i] != "|":
                    new_child[i] = "|"
                    new_child = "".join(new_child)

                    if new_child not in checked:
                        search_space.put(new_child)
    return False

def main():
    input = get_input("Day7/input.txt")
    equations = input.split("\n")

    # Attempt to find a solution equation for each target and keep track of total sum
    sum = 0
    count = 0
    for e in equations:
        count += 1
        # Check if it's solvable
        if is_solvable(e):
            # Add the target
            sum += get_target(e)
            print(sum, "|", get_target(e), "|", round(count/850 * 100, 2), "%")

    result = sum
    print(result)
        
# Run program
main()