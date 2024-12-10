# Bridge Repair
from queue import Queue

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def get_target(e):
    return int(e.split(" ")[0][:-1])

# # Did not read instructions - equations are solved left-to-right, not following BEDMAS
# def get_products(numbers, operators):
#     products = []
#     prev = int(numbers[0])
#     n = 1
#     # Linearly group numbers by *, and multiply them together
#     for muls in operators.split("+"):
#         if n < len(numbers):
#             curr = int(numbers[n])
            
#         if len(muls) > 0:
#             for i in range(0, len(muls)):
#                 prev *= curr
#                 n += 1
#                 if n < len(numbers):
#                     curr = int(numbers[n])

#         products.append(prev)
#         prev = curr
#         n += 1
#     return products

def calc(numbers, operators):
    # Calculate equation from left to right, not following BEDMAS
    result = int(numbers[0])
    for i in range(0, len(operators)):
        curr_num = int(numbers[i + 1])
        if operators[i] == "*":
            result *= curr_num
        elif operators[i] == "+":
            result += curr_num
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

        if target == calc(numbers, operators):
            # Target found
            return True
        else:
            # Target not found; Keep searching while avoiding redundant searches
            checked.add(operators)

        # Generate new nodes to search using the current operators
        for i in range(0, len(operators)):
            new_operators = [*operators] # Convert operators from string to list

            # Generate a new child node, where a + is changed to a *
            if new_operators[i] == "+":
                new_operators[i] = "*"
                new_operators = "".join(new_operators) # Convert operators from list to string
                
                # Don't bother adding the child if it's already been searched
                if new_operators not in checked:
                    search_space.put(new_operators)

    return False

def main():
    input = get_input("Day7/input.txt")
    equations = input.split("\n")

    # Attempt to find a solution equation for each target and keep track of total sum
    sum = 0
    for e in equations:
        # Check if it's solvable
        if is_solvable(e):
            # Add the target
            sum += get_target(e)

    result = sum
    print(result)
        
# Run program
main()