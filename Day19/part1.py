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
    for towel in available:
        # Avoid making too big of a towel
        if len(current) + len(towel) > len(target):
            continue

        # Only get valid children for the search
        valid = True
        for i in range(0, len(towel)):
            if towel[i] != target[len(current) + i]:
                valid = False
                break
        
        if valid:
            children.append(current + towel)

    return children

def is_makeable(pattern, available):
    search_space = Queue()
    seen = set()
    
    # Start search with any towels that could possibly start the pattern
    children = get_children("", pattern, available)
    for c in children:
        search_space.put(c)
    
    while not search_space.empty():
        current = search_space.get()
        # print(current)

        # Avoid redundant searches
        if current in seen:
            continue
        else:
            seen.add(current)

        # Pattern was successfully made using the towels given
        if current == pattern:
            return True
        
        # Generate children that could potentially create the pattern in the future
        children = get_children(current, pattern, available)
        for c in children:
            search_space.put(c)
        
    # Pattern couldn't be made
    return False

def main():
    inputs = get_input("Day19/input.txt").split("\n\n")
    available = set(inputs[0].split(", "))
    patterns = inputs[1].split("\n")

    count = 0
    for i in range(0, len(patterns)):
        pattern = patterns[i]
        if is_makeable(pattern, available):
            count += 1
        print(f"Completion: {round((i + 1) / len(patterns) * 100, 2)}%")

    print(count)

# Run program
main()