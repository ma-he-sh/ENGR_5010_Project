import matplotlib.pyplot as plt

def plot_paths( graph, cityref, bestSol, elapsed_time, plot=True ):
    print(str(int(bestSol[1])), "\t", len(bestSol[0]),"\t", elapsed_time, "\t", str(bestSol[0]) )
    #print("best solution:", str(int(bestSol[1])), str(bestSol[0]), " num trucks:", len(bestSol[0]), " elaspsed:", elapsed_time, "s")

    if plot:
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


            r = rand.random()
            b = rand.random()
            g = rand.random()
            color = (r, g, b)

            plt.plot(points["x"], points["y"], marker='o', linestyle="--", color=color)

        # draw labels
        for city in graph:
            label = cityref[city]
            plt.annotate( cityref[city], graph[city], textcoords="offset points", xytext=(0, 10), ha="center", fontsize=6 )

        #img = plt.imread("./ontario_map.jpg")
        #fig, ax = plt.subplots()

        plt.plot(deportX, deportY, marker='x')
        plt.title('Paths')
        plt.show()

def dataset( filename ):
    f = open("../dataset_generate/datasets/" + filename , "r")
    lines = f.readlines()


    capacity = 0
    datafile = ''

    NODE_SECTION = False
    DEMAND_SECTION = False
    DEPOT_SECTION = False

    graph = {}
    demand = {}
    cityref = {}

    for line in lines:
        if 'CAPACITY' in line:
            capacity = int(line.split(":")[1].strip(' '))
        
        if 'DATAFILE' in line:
            datafile = line.split(":")[1].strip(" ").rstrip("\n")

        if "NODE_COORD_SECTION" in line:
            NODE_SECTION = True

        if "DEMAND_SECTION" in line:
            NODE_SECTION = False
            DEMAND_SECTION = True

        if "DEPOT_SECTION" in line:
            NODE_SECTION = False
            DEMAND_SECTION = False
            DEPOT_SECTION = True

        if NODE_SECTION and not 'NODE_COORD_SECTION' in line:
            parts = line.split(" ")
            city = " ".join(line.split(" ", 4)[4:]).rstrip("\n")

            graph[int(parts[0])] = (float( parts[1] ), float( parts[2] ))
            cityref[int(parts[0])] = city

        if DEMAND_SECTION and not 'DEMAND_SECTION' in line:
            parts = line.split(" ")
            demand[int(parts[0])] = int(parts[1])

    return capacity, graph, demand, cityref, datafile
