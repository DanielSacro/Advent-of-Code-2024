# Red-Nosed Reports

# Running program from outside Day2 folder
def get_input(filename):
    file = open(filename, "r")
    return file.read()

def put_output(filename, output):
    file = open(filename, "a")
    file.write(output + "\n")

def verify_report(levels):
    # Compare current to previous
    prev = int(levels[0])
    first_loop = True
    increasing = True
    for i in range(1, len(levels)):
        curr = int(levels[i])
        diff = curr - prev
        if diff == 0 or abs(diff) > 3:
            return False, i
        
        if first_loop:
            if diff < 0:
                increasing = False
            first_loop = False

        if increasing and diff < 0:
            return False, i
        elif not increasing and diff > 0:
            return False, i
        
        prev = curr

    return True, -1

def main():
    input = get_input("Day2/input.txt")
    reports = input.split("\n")
    count = 0
    for r in reports:
        levels = r.split(" ")
        safe, error = verify_report(levels)
        if safe:
            count += 1
        else:
            # Eliminate first possible error found
            levels.pop(error) 
            safe, err = verify_report(levels)
            if safe:
                count += 1
                continue # Avoid redundant testing/counting

            # Attempt to eliminate indices around error
            levels = r.split(" ")
            levels.pop(error - 1) # error index is always > 0
            safe, err = verify_report(levels)
            if safe:
                count += 1
                continue

            if error + 1 < len(levels):
                levels = r.split(" ")
                levels.pop(error + 1)
                safe, err = verify_report(levels)
                if safe:
                    count += 1
                    continue

            # Attempt to tolerate one bad level
            levels = r.split(" ")
            levels.pop(0)
            safe, error = verify_report(levels)
            if safe:
                count += 1
                continue

            put_output("Day2/output.txt", r)
    
    print(count)
        
# Run program
main()