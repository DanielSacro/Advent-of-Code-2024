# Ceres Search

def get_input(filename):
    file = open(filename, "r")
    return file.read()

# For debugging
def put_output(filename, output):
    file = open(filename, "a")
    file.write(output)
    
def check_bounds(r, c, tot_rows, tot_cols):
    result = True
    if r < 0 or c < 0:
        result = False
    elif r > tot_rows - 1 or c > tot_cols - 1:
        result = False
    return result

def init_mas_grid(tot_rows, tot_cols):
    mas_grid = []
    for r in range(0, tot_rows):
        row = []
        for c in range(0, tot_cols):
            row.append(".")
        mas_grid.append(row)
    return mas_grid

def find_mas(grid):
    tot_rows = len(grid)
    tot_cols = len(grid[0])
    mas_grid = init_mas_grid(tot_rows, tot_cols)

    # Scan grid for M-A-S
    for r in range(0, tot_rows):
        for c in range(0, tot_cols):
            # Look for Ms
            if grid[r][c] != "M":
                continue

            # M found, look for As around M
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Out of bounds check
                    valid = check_bounds(r + i, c + j, tot_rows, tot_cols)
                    if not valid:
                        continue
                    elif (i == 0) and (j == 0):
                        # Only search around the M
                        continue
                    
                    # Look for A
                    if grid[r + i][c + j] != "A":
                        continue
                        
                    # A found, look for S in same direction as A
                    # Out of bounds check
                    valid = check_bounds(r + 2*i, c + 2*j, tot_rows, tot_cols)
                    if not valid:
                        continue

                    # Look for S
                    if grid[r + 2*i][c + 2*j] != "S":
                        continue

                    # S found => MAS found, save location
                    mas_grid[r][c] = "M"
                    mas_grid[r + i][c + j] = "A"
                    mas_grid[r + 2*i][c + 2*j] = "S"
    return mas_grid

def is_cross(r, c, mas_grid):
    # Cross points have to be M or S
    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            if mas_grid[r + i][c + j] == "." or mas_grid[r + i][c + j] == "A":
                return False

    # Cannot have same letters across each other (spells SAS and MAM, not MAS)
    if mas_grid[r - 1][c - 1] == mas_grid[r + 1][c + 1] or mas_grid[r - 1][c + 1] == mas_grid[r + 1][c - 1]:
        return False

    return True

def count_x(mas_grid):
    tot_rows = len(mas_grid)
    tot_cols = len(mas_grid[0])
    soln_grid = init_mas_grid(tot_rows, tot_cols)
    count = 0

    # Scan the MAS grid for crosses, starting by finding their centres
    # Omitting the first and last rows and columns from the search makes search easier (no bound checking and works correctly only for finding centres)
    for r in range(1, tot_rows - 1):
        for c in range(1, tot_cols - 1):
            # Assume the centre of 2 MAS's is always A
            if mas_grid[r][c] != "A":
                continue

            # Centre found, check if it's a valid cross
            if is_cross(r, c, mas_grid):
                soln_grid[r - 1][c - 1] = mas_grid[r - 1][c - 1]
                soln_grid[r - 1][c + 1] = mas_grid[r - 1][c + 1]
                soln_grid[r][c] = mas_grid[r][c]
                soln_grid[r + 1][c - 1] = mas_grid[r + 1][c - 1]
                soln_grid[r + 1][c + 1] = mas_grid[r + 1][c + 1]
                count += 1
    return count, soln_grid

def main():
    input = get_input("Day4/input.txt")

    # Change the input's representation into a "matrix" for easier indexing
    grid = input.split("\n")

    # Find and count how many times XMAS appears in word search
    mas_grid = find_mas(grid)
    result, soln_grid = count_x(mas_grid)

    # Debug
    # for i in range(0, len(soln_grid)):
    #     for j in range(0, len(soln_grid[0])):
    #         put_output("Day4/output.txt", soln_grid[i][j])
    #     put_output("Day4/output.txt", "\n")
    
    print(result)
        
# Run program
main()