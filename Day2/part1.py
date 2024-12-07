# Red-Nosed Reports

# Running program from outside Day2 folder
def get_input(filename):
    file = open(filename, "r")
    return file.read()

def verify_report(report):
    levels = report.split(" ")
    
    # Compare current to previous
    prev = int(levels[0])
    first_loop = True
    increasing = True
    for i in range(1, len(levels)):
        curr = int(levels[i])
        diff = curr - prev
        if diff == 0 or abs(diff) > 3:
            return False
        
        if first_loop:
            if diff < 0:
                increasing = False
            first_loop = False

        if increasing and diff < 0:
            return False
        elif not increasing and diff > 0:
            return False
        
        prev = curr

    return True  

def main():
    input = get_input("Day2/input.txt")
    reports = input.split("\n")
    count = 0
    for r in reports:
        safe = verify_report(r)
        if safe:
            count += 1
    
    print(count)
        
# Run program
main()