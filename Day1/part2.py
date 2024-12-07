# Historian Hysteria

# Running program from outside Day1 folder
file = open("Day1/input.txt", "r")
input = file.read()

# Parse the input into 2 separate lists
pairs = input.split("\n")
list1 = []
list2 = {}
for p in pairs:
    nums = p.split("   ")
    n1 = int(nums[0])
    n2 = int(nums[1])

    list1.append(n1)
    # Count frequency
    if n2 in list2:
        list2[n2] += 1
    else:
        list2[n2] = 1

similarity = 0
for n in list1:
    if n in list2:
        similarity += n * list2[n]

print(similarity)