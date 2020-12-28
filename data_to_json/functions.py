import random as rand

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
    indexes = {}

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
            indexes[int(parts[0])] = parts[3]

        if DEMAND_SECTION and not 'DEMAND_SECTION' in line:
            parts = line.split(" ")
            demand[int(parts[0])] = int(parts[1])

    return capacity, graph, demand, cityref, indexes, datafile
