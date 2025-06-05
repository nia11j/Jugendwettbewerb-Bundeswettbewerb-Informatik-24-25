import sys

def hauptfunktion(p1, p2):
    list1 = [(["D"], ((0, 0), (0, 0)))]
    list2 = []
    goal = (p1["size"][0] - 1, p1["size"][1] - 1)
    visited = set()
    while list1:
        while list1:
            lastpath = list1.pop(0)
            locations = lastpath[1]
            possibilities = nextpossiblefields(p1, p2, locations)
            for direction in possibilities:
                nextpath = lastpath[0].copy()
                nextpath.append(direction)
                nextlocations = possibilities[direction]
                if nextlocations == (goal, goal):
                    return nextpath[1:]
                if not nextlocations in visited:
                    visited.add(nextlocations)
                    list2.append((nextpath, nextlocations))
        list1, list2 = list2, list1
    return []

def nextpossiblefields(p1, p2, locations):
    width = p1["size"][0]
    height = p1["size"][1]
    returndict = {}
    directions = ["R", "L", "U", "D"]
    for direction in directions:
        if has_barrier(p1, locations[0], direction) or locations[0] == (width - 1, height - 1):
            newlocation1 = locations[0]
        else:
            newlocation1 = nextlocation(locations[0], direction)
        if has_barrier(p2, locations[1], direction) or locations[1] == (width - 1, height - 1):
            newlocation2 = locations[1]
        else:
            newlocation2 = nextlocation(locations[1], direction)
        if (newlocation1, newlocation2) != locations:
            returndict[direction] = (newlocation1, newlocation2)
    return returndict
    
def nextlocation(location, direction):
    if direction == "D":
        return (location[0], location[1] + 1)
    if direction == "U":
        return (location[0], location[1] - 1)
    if direction == "L":
        return (location[0] - 1, location[1])
    if direction == "R":
        return (location[0] + 1, location[1])

def has_barrier(labyrinth, location, direction):
    if direction == "D":
        if location[1] >= height - 1:
            return True
        return labyrinth["horizontal_barriers"][location[1]][location[0]] == 1
    if direction == "L":
        if location[0] <= 0:
            return True
        return labyrinth["vertical_barriers"][location[1]][location[0] - 1] == 1
    if direction == "R":
        if location[0] >= width - 1:
            return True
        return labyrinth["vertical_barriers"][location[1]][location[0]] == 1
    if direction == "U":
        if location[1] <= 0:
            return True
        return labyrinth["horizontal_barriers"][location[1] - 1][location[0]] == 1

file = open(sys.argv[1], "r")
grubenort1 = []
grubenort2 = []
lines = [l.rstrip() for l in file.readlines()]
(width, height) = [int(l) for l in lines[0].split(" ")]
lines = lines[1:]
lines = [[int(width) for width in line.split(" ")]for line in lines]
vertical1 = lines[0:height]
lines = lines[height:]
horizontal1 = lines[0:height-1]
lines = lines[height-1:]
gruben1 = int(lines[0][0])
lines = lines[1:]
if gruben1 > 0:
    for z in range(gruben1):
        grubenort1.append(lines[z])
    lines = lines[z+1:]
else:
    lines = lines[:]
vertical2 = lines[0:height]
lines = lines[height:]
horizontal2 = lines[0:height-1]
lines = lines[height-1:]
gruben2 = int(lines[0][0])
lines = lines[1:]
if gruben2 > 0:
    for z in range(gruben2):
        grubenort2.append(lines[z])
    lines = lines[z+1:]
else:
    lines = lines[:]
labyrinth1 = {"size": (width, height), "vertical_barriers": vertical1, "horizontal_barriers": horizontal1, "pits": grubenort1}
labyrinth2 = {"size": (width, height), "vertical_barriers": vertical2, "horizontal_barriers": horizontal2, "pits": grubenort2}
print("Der Pfad lautet: " + ", ".join(hauptfunktion(labyrinth1, labyrinth2)))