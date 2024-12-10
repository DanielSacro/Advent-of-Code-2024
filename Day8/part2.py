# Resonant Collinearity
from queue import Queue

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def get_antennas(grid):
    antennas = {}
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            spot = grid[i][j]
            if spot == "." or spot == "#":
                # Not an antenna, keep scanning
                continue
            
            if spot not in antennas:
                antennas[spot] = []
            
            antennas[spot].append((i, j))
    return antennas

def is_valid_antinode(antinode, tot_rows, tot_cols):
    return -1 < antinode[0] and antinode[0] < tot_rows and -1 < antinode[1] and antinode[1] < tot_cols

def generate_antinode(antenna1, antenna2, tot_rows, tot_cols):
    antinodes = []
    r_diff = antenna2[0] - antenna1[0]
    c_diff = antenna2[1] - antenna1[1]

    # Generate antinodes in the direction of antenna1 until they go out of bounds
    n = 0
    antinode = (antenna1[0] - r_diff, antenna1[1] - c_diff)
    while is_valid_antinode(antinode, tot_rows, tot_cols):
        # Last antinode is valid, so add it
        antinodes.append(antinode)

        # Get next antinode and re-check it afterwards
        n += 1
        antinode = (antenna1[0] - n * r_diff, antenna1[1] - n * c_diff)


    # Generate antinodes in the direction of antenna2 until they go out of bounds
    n = 0
    antinode = (antenna2[0] + r_diff, antenna2[1] + c_diff)
    while is_valid_antinode(antinode, tot_rows, tot_cols):
        # Last antinode is valid, so add it
        antinodes.append(antinode)

        # Get next antinode and re-check it afterwards
        n += 1
        antinode = (antenna2[0] + n * r_diff, antenna2[1] + n * c_diff)

    # The antennas themselves are also antinodes
    if antenna1 not in antinodes:
        antinodes.append(antenna1)
        
    if antenna2 not in antinodes:
        antinodes.append(antenna2)

    return antinodes

def get_antinodes(antennas, tot_rows, tot_cols):
    valid_antinodes = set()
    for i in range(0, len(antennas) - 1):
        antenna1 = antennas[i]
        for j in range(i + 1, len(antennas)):
            antenna2 = antennas[j]
            antinodes = generate_antinode(antenna1, antenna2, tot_rows, tot_cols)

            if len(antinodes) == 0:
                # No antinodes were generated
                continue

            for a in antinodes:
                if a not in valid_antinodes:
                    valid_antinodes.add(a)

    return valid_antinodes

def main():
    input = get_input("Day8/input.txt")
    grid = input.split("\n")
    
    # Get the locations of each antenna for each frequency
    antennas = get_antennas(grid)

    # Generate all the antinodes for each frequency, and count each valid antinode (i.e. within bounds)
    antinode_locations = set()
    for frequency in antennas:
        if len(antennas[frequency]) > 1:
            antinodes = get_antinodes(antennas[frequency], len(grid), len(grid[0]))
            for a in antinodes:
                if a not in antinode_locations:
                    antinode_locations.add(a)

    result = len(antinode_locations)
    print(result)
        
# Run program
main()