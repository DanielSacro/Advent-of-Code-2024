# Historian Hysteria
import heapq


# Running program from outside Day1 folder
file = open("Day1/input.txt", "r")
input = file.read()

# Parse the input into 2 separate lists
pairs = input.split("\n")
list1 = []
list2 = []
for p in pairs:
    nums = p.split("   ")
    heapq.heappush(list1, int(nums[0]))
    heapq.heappush(list2, int(nums[1]))

tot_distance = 0
for i in range(0, len(list1)):
    tot_distance += abs(heapq.heappop(list1) - heapq.heappop(list2))

print(tot_distance)