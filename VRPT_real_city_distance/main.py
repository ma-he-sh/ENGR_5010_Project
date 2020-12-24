from acovrp import ACOVRP
from functions import dataset

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import random as rand

import time

def plot_paths( graph, cityref, bestSol, elapsed_time, plot=True ):
    #print( "bestSol", bestSol )
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

if __name__ == '__main__':
    """
    PARAMS
    alpha:  relative importance of pheromone
    beta:   relative importance of heuristic information 
    sigma:  
    rho:    pheromone coefficient :: evaporation factor
    theta:
    num_ants: number of ants
    MAX_NFC: max number of function calls
    """

    capacity, graph, delivery_demand, cityref, datafile = dataset('data_1_23.txt')
    #print( graph )

    alpha = 1                   # 1
    # --------------------------------
    beta = 5                    # 5
    # --------------------------------
    sigma = 4                   # 4
    # --------------------------------
    rho = 0.1                   # 0.1
    # --------------------------------
    theta = 80                  # 80
    # --------------------------------
    num_ants = 40               # 40
    # --------------------------------
    MAX_NFC = 100               # 100
    # --------------------------------
    vehicle_capacity = 2000     # 2000

    
    # --------------------------------
    tempdata = pd.read_csv( "../helpers/raw_data/" + datafile )
    citydata = tempdata.set_index("x")

    #for num_ants in [40, 60, 100, 200]:
    #for MAX_NFC in [200, 400, 1000, 2000]:
    #for rho in [0.02, 0.1, 0.5, 0.8]:
    #for beta in [1, 3, 5, 10]:
    #for alpha in [0.5, 1, 2, 3]:
    for vehicle_capacity in [1000, 1500, 2500, 2745, 4000, 11000, 15000]:
        vrp = ACOVRP( alpha, beta, sigma, rho, theta, num_ants, vehicle_capacity, delivery_demand, cityref, citydata, MAX_NFC )
        vrp.set_graph( graph )
        
        start_time   = time.time()
        bestSol = vrp.process()
        elapsed_time = (time.time() - start_time )


        finalSol = vrp.get_cost_from_depot()
        print( "final:", finalSol )
        print( "best:", bestSol )

        if bestSol is not None:
            plot_paths( graph, cityref, bestSol, elapsed_time, True )
