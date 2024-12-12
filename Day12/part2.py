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

def count_sides(perimeter):
    total_sides = 0

    # Frequency of a perimeter tuple = how many sides are caused in the perimeter coordinate (like sweeper)
    # Example: If a perimeter tuple shows up 3 times in the perimeter variable, there are 3 sides associated with that perimeter tuple
    freq = {}
    for p in perimeter:
        if p not in freq:
            freq[p] = 1
        else:
            freq[p] += 1

    # Find vertical sides
    verticals = set()
    for p in freq:
        if p in verticals:
            continue

        # Choose a perimeter tuple not yet associated with a side
        if freq[p] > 0:
            r = p[0]
            c = p[1]

            # Associate this tuple with one vertical side
            freq[p] -= 1

            # Find top portions of perimeter tuple to form top portion of side
            top = r - 1
            while (top, c) in perimeter:
                # Perimeter tuple above is already associated with other sides
                if freq[(top, c)] == 0:
                    break

                # Otherwise, there's a connecting perimeter tuple above that can be associated with the same vertical side
                freq[(top, c)] -= 1
                verticals.add((top, c))
                top -= 1
                # Stop when there is no connecting perimeter tuple on above

            # Find bottom portions of perimeter tuple to form right portion of side
            bottom = r + 1
            while (bottom, c) in perimeter:
                # Perimeter tuple below is already associated with other sides
                if freq[(bottom, c)] == 0:
                    break

                # Same as before, there's a connecting perimeter tuple below that can be associated with the same vertical side
                freq[(bottom, c)] -= 1
                verticals.add((bottom, c))
                bottom += 1
                # Stop when there is no connecting perimeter tuple below

            if top == r - 1 and bottom == r + 1:
                # No connecting horizontal tuples, so this tuple might be part of a horizontal side
                freq[p] += 1
            else:
                # Otherwise, count this vertical side as a unique side
                total_sides += 1
                verticals.add(p)
    big_verticals = total_sides
    # print("Big vertical sides:", big_verticals)
    # print(freq)

    # Find horizontal sides (same as before, but with columns; looking left and right)
    horizontals = set()
    for p in freq:
        if p in horizontals:
            continue

        if freq[p] > 0:
            r = p[0]
            c = p[1]

            # Associate this tuple with one horizontal side
            freq[p] -= 1

            left = c - 1
            while (r, left) in perimeter:
                if freq[(r, left)] == 0:
                    break
                freq[(r, left)] -= 1
                horizontals.add((r, left))
                left -= 1
                

            right = c + 1
            while (r, right) in perimeter:
                if freq[(r, right)] == 0:
                    break
                freq[(r, right)] -= 1
                horizontals.add((r, right))
                right += 1

            if left == c - 1 and right == c + 1:
                # No connecting horizontal tuples
                freq[p] += 1
            else:
                # Otherwise, count this horizontal side as a unique side
                total_sides += 1
                horizontals.add(p)
    big_horizontals = total_sides - big_verticals
    # print("Big horizontal sides:", big_horizontals)
    # print(freq)

    # Remaining tuples were not part of a bigger horizontal or vertical side; they are their own single-tuple sides
    for p in freq:
        if freq[p] > 0:
            total_sides += freq[p]
    if (total_sides % 2) != 0:
        print(freq)
        print("Big verticals sides:", big_verticals)
        print("Big horizontal sides:", big_horizontals)
        print("Horizonals:", horizontals)
        print("Small sides:", total_sides - big_horizontals - big_verticals)
    # print(freq)

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
    sides = count_sides(outer_layer)
    price = area * sides
    if sides % 2 == 1:
        print("Start:", start)
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