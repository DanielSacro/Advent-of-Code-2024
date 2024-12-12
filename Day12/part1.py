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

def get_region_and_price(start, grid):
    r = start[0]
    c = start[1]
    plant = grid[r][c]

    search_space = Queue()
    search_space.put(start)

    perimeter = 0

    # Get the region of the plot
    region = []
    visited = set()
    while not search_space.empty():
        plot = search_space.get()
        r = plot[0]
        c = plot[1]

        # Visits that are out of bounds contribute to perimeter, not region
        if not (-1 < r and r < len(grid) and -1 < c and c < len(grid[0])):
            perimeter += 1
            continue

        # Visits to plots that don't have the same plant also contribute to perimeter
        if grid[r][c] != plant:
            perimeter += 1
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
    price = area * perimeter
    # print(plant, region, area, perimeter, price)
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