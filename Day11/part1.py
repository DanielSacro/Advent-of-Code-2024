# Plutonian Pebbles

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def remove_leading_zeros(stone):
    new_stone = ""
    leading_zeros_present = True
    for c in stone:
        if leading_zeros_present:
            if c == "0":
                continue
            else:
                new_stone += c
                leading_zeros_present = False
        else:
            new_stone += c

    # If stone was all zeros, return just one zero
    if len(new_stone) == 0:
        new_stone += "0"

    return new_stone

def evolve(stone):
    result = []
    if stone == "0":
        result.append("1")
    elif len(stone) % 2 == 0:
        first_half = stone[0:len(stone)//2]
        second_half = stone[len(stone)//2:]

        # Eliminate leading zeros in second half
        second_half = remove_leading_zeros(second_half)

        result.append(first_half)
        result.append(second_half)
    else:
        result.append(str(int(stone) * 2024))
    return result

def change_stones(stones):
    new_stones = []
    
    for s in stones:
        new_stones.extend(evolve(s))
    
    return new_stones

def main():
    input = get_input("Day11/input.txt")
    stones = input.split(" ")
    blinks = 25

    # print(f'Starting: \t{stones}')
    for i in range(0, blinks):
        stones = change_stones(stones)
        # print(f'Blink #{i+1}: \t{stones}')
    
    result = len(stones)
    # print(f'Result: \t{stones}')
    print(result)
        
# Run program
main()