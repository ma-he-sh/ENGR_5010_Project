from acovrp import ACOVRP
from functions import dataset

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import random as rand

def plot_paths( graph, cityref, bestSol ):
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
    rho:    pheromone coefficient
    theta:
    num_ants: number of ants
    MAX_NFC: max number of function calls
    """

    vehicle_capacity = 2000
    capacity, graph, delivery_demand, cityref, datafile = dataset('data_3_96.txt');
    #print( graph )

    alpha = 2
    beta = 5
    sigma = 3
    rho = 0.8
    theta = 80
    num_ants = 22
    MAX_NFC = 10

    vrp = ACOVRP( alpha, beta, sigma, rho, theta, num_ants, vehicle_capacity, delivery_demand, cityref, datafile, MAX_NFC )
    vrp.set_graph( graph )
    bestSol = vrp.process()
    
    if bestSol is not None:
        plot_paths( graph, cityref, bestSol )