import matplotlib.pyplot as plt
import random as rand
import re

def plot_paths( graph, bestSol ):
    print("best solution:", str(int(bestSol[1])), str(bestSol), " num trucks:", len(bestSol[0]))

    # deport location
    deportX, deportY = graph.get(1)

    for i in range(0, len(bestSol[0])):

        points = {
            "x": [],
            "y": []
        }

        # start point
        points["x"].append(deportX)
        points["y"].append(deportY)

        for j in range(0, len(bestSol[0][i]) - 1):
            pathFrom = bestSol[0][i][j]
            pathTo = bestSol[0][i][j + 1]

            x1, y1 = graph[pathFrom]
            x2, y2 = graph[pathTo]
            # print( x1, x2, y1, y2 )

            points["x"].append(x1)
            points["y"].append(y1)
            points["x"].append(x2)
            points["y"].append(y2)

        # end point
        points["x"].append(deportX)
        points["y"].append(deportY)

        plt.plot(points["x"], points["y"], marker='o', linestyle="--")

    plt.plot(deportX, deportY, marker='x')
    plt.title('Paths')
    plt.show()

def dataset( filename ):
    f = open("./dataset/" + filename , "r")
    content = f.read()
    optimalValue = re.search("Optimal value: (\d+)", content, re.MULTILINE)
    if(optimalValue != None):
        optimalValue = optimalValue.group(1)
    else:
        optimalValue = re.search("Best value: (\d+)", content, re.MULTILINE)
        if(optimalValue != None):
            optimalValue = optimalValue.group(1)
    capacity = re.search("^CAPACITY : (\d+)$", content, re.MULTILINE).group(1)
    graph = re.findall(r"^(\d+) (\d+) (\d+)$", content, re.MULTILINE)
    demand = re.findall(r"^(\d+) (\d+)$", content, re.MULTILINE)
    graph = {int(a):(int(b),int(c)) for a,b,c in graph}
    demand = {int(a):int(b) for a,b in demand}
    capacity = int(capacity)
    optimal = int(optimalValue)
    return capacity, graph, demand, optimal

