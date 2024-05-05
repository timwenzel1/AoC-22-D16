# Advent of Code 22 Day 16 Part 2

from collections import deque
import more_itertools as mit
import itertools

import time
start_time = time.time()

#opens the file and saves the text in puzzleInput
file = open('big_input.txt')
puzzleInput = file.readlines()
puzzleInputLines = len(puzzleInput)
file.close()


#initialies the valves dictionary
valves = {}


#fill the dictonary by extracting the valve, flow rate and lead to from the puzzle input
for i in range (0,puzzleInputLines):
    string = puzzleInput[i]
    string = string.split("Valve ", 1)[1]
    Valve = string.split(" has flow", 1)[0]
    string = string.split(" has flow rate=", 1)[1]
    flowRate = string.split(";", 1)[0]
    leadTo = string.split(" ", 5)[5]
    leadTo = leadTo.split("\n", 1)[0]
    leadTo = leadTo.split(", ")
    valves[Valve] = int(flowRate), leadTo

#print(valves)

# distances is an dictionary which stores the distances between pressure releasing Valves
distances = {}

for valve in valves:
    if valve != "AA" and valves[valve][0] == 0: #sort out all the Valves which do not release any pressure
        continue

    distances[valve] = {}
    visited = {valve}
    queue = deque([(0, valve)])                 #deque used to delete nodes at the front and add new nodes at the end

    while len(queue) > 0:
        distance, position = queue.popleft()    # save the distance and position of the Valve we are currently looking at from the "Start-Valve" (not necessary AA)
        for neighbour in valves[position][1]:
            if neighbour in visited:
                continue                        #if the neigbour is already visited skip the current loop iteration
            visited.add(neighbour)              # add the neighbour to the visited set
            if valves[neighbour][0] > 0:
                distances[valve][neighbour] = distance + 1
            queue.append((distance + 1, neighbour))

#print(distances)


visitedValves = set()

def dfs(time, valve, visitedValves):
    maxPressure = 0
    for neighbour in distances[valve]:
        if neighbour in visitedValves:
            continue
        remainingTime = time - distances[valve][neighbour] - 1
        if remainingTime <= 0:
            continue
        visitedValves.add(neighbour)
        maxPressure = max(maxPressure, dfs(remainingTime, neighbour, visitedValves) + valves[neighbour][0] * remainingTime)
        visitedValves.remove(neighbour) 
    return maxPressure




valvesWithPressure = set()
for valve, data in valves.items():
    pressure = data[0]
    if pressure > 0:
        valvesWithPressure.add(valve)


maxPressure = 0

#x = ([part for k in range(1, len(valvesWithPressure) + 1) for part in mit.set_partitions(valvesWithPressure, k)])

def unique_partitions(s):
    n = len(s)
    for r in range(1, n // 2 + 1):
        for subset in itertools.combinations(s, r):
            remaining = s - set(subset)
            yield (set(subset), remaining)

x = list(unique_partitions(valvesWithPressure))

for i in range (0, len(x)):
    set1 = x[i][0]
    set2 = valvesWithPressure - set1
    maxPressure = max(maxPressure, dfs(26,'AA', set1) + dfs(26,'AA',set2))
    print(i)

print(maxPressure)


print("--- %s seconds ---" % (time.time() - start_time))









