# Disk Fragmenter

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def expand(disk_map):
    data = []
    file_ID = 0
    for i in range(0, len(disk_map)):
        data_length = int(disk_map[i])
        if i % 2 == 0:
            # Even index = file
            for j in range(0, data_length):
                file_data = str(file_ID)
                data.append(file_data)
            file_ID += 1
        else:
            # Odd index = free space
            for j in range(0, data_length):
                data.append(".")
    
    return data

def defragment(data):
    left = 0 
    right = len(data) - 1
    while left < right:
        # Find left-most "." value first
        if data[left] != ".":
            left += 1
            continue

        # Get the right-most non "." value
        while data[right] == ".":
            right -= 1
            # No error check - assume right never exceeds left (left should move passed right first)
        
        # Switch their spots
        data[left] = data[right]
        data[right] = "."
    return data

def get_checksum(data):
    checksum = 0
    for i in range(0, len(data)):
        if data[i] == ".":
            # No more numbers to check
            break

        checksum += i * int(data[i])

    return checksum

def main():
    input = get_input("Day9/input.txt")
    disk_map = input

    # Expand disk map
    data = expand(disk_map)
    # print("".join(data))

    # Defragment
    new_data = defragment(data)
    # print("".join(new_data))

    # Checksum
    result = get_checksum(new_data)

    print(result)
        
# Run program
main()