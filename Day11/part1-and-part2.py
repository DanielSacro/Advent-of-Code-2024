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

solutions = {}
def evolve(stone):
    if stone in solutions:
        return solutions[stone]

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

    # Memoize
    solutions[stone] = result
    return result

def change_stones(stones):
    new_stones = {}
    
    for s in stones:
        tot_s = stones[s]
        stones_to_add = evolve(s)
        for new_s in stones_to_add:
            if new_s not in new_stones:
                new_stones[new_s] = 1 * tot_s
            else:
                new_stones[new_s] += 1 * tot_s
    
    return new_stones

def count_stones(stones):
    count = 0
    for s in stones:
        count += stones[s]
    return count

def main():
    input = get_input("Day11/input.txt")
    stones = {}
    for s in input.split(" "):
        if s not in stones:
            stones[s] = 1
        else:
            stones[s] += 1

    # print(f'Starting: \t{stones}')
    blinks = 75
    for i in range(0, blinks):
        stones = change_stones(stones)
        print(f"Blink #{i + 1}")
        # print(f'Blink #{i+1}: \t{stones}')
    
    result = count_stones(stones)
    # print(f'Result: \t{stones}')
    print(result)
        
# Run program
main()