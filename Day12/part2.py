# Garden Groups
from queue import Queue

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def get_neighbors(plot):
    neighbors = []
    r = plot[0]
    c = plot[1]

    neighbors.append((r - 1, c)) # Top
    neighbors.append((r + 1, c)) # Bottom
    neighbors.append((r, c - 1)) # Left
    neighbors.append((r, c + 1)) # Right

    return neighbors

# Counting sides using hint from Reddit (# sides = # corners)
def count_sides(region, perimeter):
    if len(region) == 1:
        return 4

    # Count "convex" corners
    convex_corners = 0
    for plot in region:
        neighbors = get_neighbors(plot)
        
        fences = []
        for n in neighbors:
            if n in perimeter:
                fences.append(n)
        
        # Count corners
        if len(fences) == 4:
            # Plot is fenced off on all sides
            convex_corners += 4
        elif len(fences) == 3:
            # Any configuration of 3 fences around a plot = 2 corners
            convex_corners += 2
        elif len(fences) == 2:
            fence1 = fences[0]
            fence2 = fences[1]
            if fence1[0] != fence2[0] and fence1[1] != fence2[1]:
                convex_corners += 1

        # 1 Fence alone does not create a corner
    
    # Count "concave" corners

    seen = {}
    concave_corners = 0
    for p in perimeter:
        if p not in seen:
            seen[p] = 1
        else:
            # concave_corners.append(p)
            seen[p] += 1

    for s in seen:
        if seen[s] == 1:
            continue
        elif seen[s] == 4:
            concave_corners += 4
        else:
            concave_corners += seen[s] - 1

    # total_sides = len(convex_corners) + len(concave_corners)
    total_sides = convex_corners + concave_corners

    if total_sides % 2 == 0:
        print(perimeter)
        print("convex:", convex_corners)
        print("concave:", concave_corners)
    return total_sides

def get_region_and_price(start, grid):
    r = start[0]
    c = start[1]
    plant = grid[r][c]

    search_space = Queue()
    search_space.put(start)

    # Get the region of the plot
    region = []
    visited = set()
    outer_layer = []
    while not search_space.empty():
        plot = search_space.get()
        r = plot[0]
        c = plot[1]

        # Visits that are out of bounds contribute to perimeter, not region
        if not (-1 < r and r < len(grid) and -1 < c and c < len(grid[0])):
            outer_layer.append(plot)
            continue

        # Visits to plots that don't have the same plant also contribute to perimeter
        if grid[r][c] != plant:
            outer_layer.append(plot)
            continue

        # Ignore redundant visits for plots already in the region
        if plot in visited:
            continue

        # Otherwise, plot has same plant, so include plot in the region and look for more connecting plants around it
        region.append(plot)

        # Generate neighboring plots
        neighbors = get_neighbors(plot)
        for n in neighbors:
            # Only visit plot if it hasn't been visited before
            if n not in visited:
                search_space.put(n)

        # Remember that we visited this plot
        visited.add(plot)

    # Calculate the price of the region
    area = len(region)
    sides = count_sides(region, outer_layer)
    price = area * sides
    if sides % 2 == 1:
        print("Start:", start)
        print(region)
        print(plant, "region's sides:", sides, "\n")
    return region, price

def get_prices(grid):
    visited = set()
    prices = {}
    # Scan the grid for plots we haven't visited yet
    for r in range(0, len(grid)):
        for c in range(0, len(grid[0])):
            curr_plot = (r, c)
            plant = grid[r][c]

            # Ignore plots that are already part of a region
            if curr_plot in visited:
                continue

            # Otherwise, we haven't visited it yet, so visit all nodes around it to form a region
            region, price = get_region_and_price(curr_plot, grid)

            # Note that we visited all plots in this region
            for plot in region:
                visited.add(plot)
            
            # Remember the region's price (organized by plant type, not by distinct region)
            if plant not in prices:
                prices[plant] = price
            else:
                prices[plant] += price
    return prices

def main():
    input = get_input("Day12/input.txt")
    grid = input.split("\n")
    # Get price of each region in grid
    prices = get_prices(grid)

    # Tally up prices
    total = 0
    for p in prices:
        total += prices[p]

    result = total
    print(result)
        
# Run program
main()