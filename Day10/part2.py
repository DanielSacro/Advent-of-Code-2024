# Hoof It
from queue import Queue

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def get_trailheads(grid):
    trailheads = []
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "0":
                trailheads.append((i, j))
    return trailheads

def get_children(node, tot_rows, tot_cols):
    i = node[0]
    j = node[1]
    children = []

    # Top child
    if i > 0:
        children.append((i - 1, j))

    # Bottom child
    if i < tot_rows - 1:
        children.append((i + 1, j))

    # Left child
    if j > 0:
        children.append((i, j - 1))

    # Right child
    if j < tot_cols - 1:
        children.append((i, j + 1))

    return children

def get_rating(trailhead, grid):
    search_space = Queue()
    search_space.put(trailhead)

    rating = 0
    while not search_space.empty():
        curr = search_space.get()
        i = curr[0]
        j = curr[1]

        if grid[i][j] == "9":
            # Reached the end of a trail
            rating += 1
            continue

        # Keep traversing by generating children nodes
        children = get_children(curr, len(grid), len(grid[0]))
        for c in children:
            k = c[0]
            l = c[1]

            # Debug
            if grid[k][l] == ".":
                continue
            
            # Can only traverse child node if height increases by 1
            if int(grid[k][l]) - int(grid[i][j]) != 1:
                continue

            # Accept redundant children to find distinct paths
            search_space.put(c)

    return rating

def main():
    input = get_input("Day10/input.txt")
    grid = input.split("\n")

    # Get trailheads
    trailheads = get_trailheads(grid)

    # Find the score of each trail head, and total it up
    total_rating = 0
    for t in trailheads:
        total_rating += get_rating(t, grid)

    result = total_rating
    print(result)
        
# Run program
main()