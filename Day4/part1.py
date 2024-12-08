# Ceres Search

def get_input(filename):
    file = open(filename, "r")
    return file.read()

# For debugging
def put_output(filename, output):
    file = open(filename, "w")
    file.write(output)
    
def check_bounds(r, c, tot_rows, tot_cols):
    result = True
    if r < 0 or c < 0:
        result = False
    elif r > tot_rows - 1 or c > tot_cols - 1:
        result = False
    return result

def count_xmas(grid):
    tot_rows = len(grid)
    tot_cols = len(grid[0])

    # Scan grid for X-M-A-S
    count = 0
    for r in range(0, tot_rows):
        for c in range(0, tot_cols):
            # Look for Xs
            if grid[r][c] != "X":
                continue

            # X found, look for Ms around X
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Out of bounds check
                    valid = check_bounds(r + i, c + j, tot_rows, tot_cols)
                    if not valid:
                        continue
                    elif (i == 0) and (j == 0):
                        # Only search around the X
                        continue
                    
                    # Look for M
                    if grid[r + i][c + j] != "M":
                        continue
                        
                    # M found, look for A in same direction as M
                    # Out of bounds check
                    valid = check_bounds(r + 2*i, c + 2*j, tot_rows, tot_cols)
                    if not valid:
                        continue

                    # Look for A
                    if grid[r + 2*i][c + 2*j] != "A":
                        continue

                    # A found, look for S in same direction as A
                    # Out of bounds check again
                    valid = check_bounds(r + 3*i, c + 3*j, tot_rows, tot_cols)
                    if not valid:
                        continue

                    # Look for S
                    if grid[r + 3*i][c + 3*j] != "S":
                        continue

                    count += 1
    return count

def main():
    input = get_input("Day4/input.txt")

    # Change the input's representation into a "matrix" for easier indexing
    grid = input.split("\n")

    # Find and count how many times XMAS appears in word search
    result = count_xmas(grid)
    print(result)
        
# Run program
main()