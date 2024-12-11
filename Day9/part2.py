# Disk Fragmenter

def get_input(filename):
    file = open(filename, "r")
    return file.read()

def expand(disk_map):
    data = []
    file_ID = 0
    for i in range(0, len(disk_map)):
        data_length = int(disk_map[i])
        data_block = []
        if i % 2 == 0:
            # Even index = file
            for j in range(0, data_length):
                file_data = str(file_ID)
                data_block.append(file_data)
            file_ID += 1
            if len(data_block) > 0:
                data.append(data_block)
        else:
            # Odd index = free space
            for j in range(0, data_length):
                data.append(["."])
    
    return data

def find_free_space(data, space_needed):
    count = 0
    for i in range(0, len(data)):
        if data[i][0] == ".":
            count += 1
            if count == space_needed:
                # Return starting index of the free space
                return i - (space_needed - 1)
        else:
            count = 0
    # No free space found
    return -1

def defragment(data):
    # Move the right-most file data blocks into the left-most free space that fits it
    for right in range(len(data) - 1, -1, -1):
        # Progress bar
        print(f'Defragmenting... {round((1 - right/len(data)) * 100, 2)}%')
        # Ignore free space
        if data[right][0] == ".":
            continue
        else:
            file_data_block = data[right]
        
        # Try to find a free space that fits the data block
        free_space_index = find_free_space(data, len(file_data_block))
        if free_space_index == -1:
            # No free space fits the data block
            continue
        elif free_space_index > right:
            continue

        # Move data block to free space
        new_data = []
        new_data.extend(data[0:free_space_index]) # Start to new file data location | good

        new_data.append(file_data_block) # File data | good

        new_data.extend(data[(free_space_index + len(file_data_block)):right]) # End of new file data location to start of old file data location |good

        for i in range(0, len(file_data_block)):
            new_data.append(["."]) # Old file data location, which is now free space

        if right != len(data) - 1:
            new_data.extend(data[(right + 1):]) # Rest of data after recently moved file data

        data = new_data
        # print(f'Moved {"".join(file_data_block)}: \t', format(data))
    return data

# For debugging
def format(data):
    result = ""
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            result += data[i][j]
    return result

def get_checksum(data):
    checksum = 0
    index = 0
    for data_block in data:
        # Ignore free space
        if data_block[0] == ".":
            for i in range(0, len(data_block)):
                index += 1
            continue

        for file_data in data_block:
            checksum += index * int(file_data)
            index += 1

    return checksum

def main():
    input = get_input("Day9/input.txt")
    disk_map = input

    # Expand disk map
    data = expand(disk_map)
    # print("Starting: \t", format(data))

    # Defragment
    new_data = defragment(data)
    # print(format(new_data))

    # Checksum
    result = get_checksum(new_data)

    print(result)
        
# Run program
main()