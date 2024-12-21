# Linen Layout
from queue import Queue

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def put_output(filename, output):
    file = open(filename, "a")
    file.write(output)

def clear_output(filename):
    file = open(filename, "w")
    file.write("")

def get_children(current, target, available):
    children = []
    current_len = len("".join(current))
    for towel in available:
        # Avoid making too big of a towel
        if current_len + len(towel) > len(target):
            continue

        # Only get valid children for the search
        valid = True
        for i in range(0, len(towel)):
            if towel[i] != target[current_len + i]:
                valid = False
                break
        
        if valid:
            child = []
            child.extend(current)
            child.append(towel) # A series of towels that form the pattern
            children.append(child) # A list of each different combination of towels that form the pattern

    return children

def count_solutions(pattern, available):
    search_space = Queue()
    seen = set()
    
    # Start search with any towels that could possibly start the pattern
    children = get_children([], pattern, available)
    for c in children:
        search_space.put(c)

    count = 0
    while not search_space.empty():
        current = search_space.get()

        # Avoid redundant searches
        if tuple(current) in seen:
            continue
        else:
            seen.add(tuple(current))

        # Pattern was successfully made using the towels given
        a = "".join(current)
        print(a)
        if a == pattern:
            print(current)
            count += 1
            continue
        
        # Generate children that could potentially create the pattern in the future
        children = get_children(current, pattern, available)
        for c in children:
            search_space.put(c)

    return count

def main():
    inputs = get_input("Day19/input.txt").split("\n\n")
    available = set(inputs[0].split(", "))
    patterns = inputs[1].split("\n")

    count = 0
    for i in range(0, len(patterns)):
        pattern = patterns[i]
        count += count_solutions(pattern, available)
        print(f"Completion: {round((i + 1) / len(patterns) * 100, 2)}%")

    print(count)

# Run program
main()