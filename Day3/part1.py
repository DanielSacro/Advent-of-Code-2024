# Mull It Over

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def main():
    input = get_input("Day3/input.txt")

    # Scan input for anything resembling mul(x,y) where x and y are integers
    result = 0
    while len(input) != 0:
        mul_start = input.find("mul(")
        if mul_start == -1:
            break # No more mul() instructions

        # Get first number if possible
        x = ""
        i = 0
        for i in range(0, 4):
            c = input[mul_start + 4 + i]
            if c.isnumeric():
                x += c
            else:
                break
        
        # Format doesn't follow
        if c != "," or len(x) == 0:
            # Stop current search and look for other mul()'s
            input = input[(mul_start + 4)::]
            continue

        # Get second number if possible
        y = ""
        for j in range(0, 4):
            c = input[mul_start + 4 + len(x) + 1 + j]
            if c.isnumeric():
                y += c
            else:
                break
        
        # Format doesn't follow
        if c != ")" or len(y) == 0:
            input = input[(mul_start + 4)::]
            continue

        result += int(x) * int(y)
        input = input[(mul_start + 4)::]
    print(result)
        
# Run program
main()