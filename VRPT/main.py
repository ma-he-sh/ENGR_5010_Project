from acovrp import ACOVRP
from functions import dataset

import numpy as np
import matplotlib.pyplot as plt

def plot_paths( graph, bestSol ):
    print("best solution:", str(int(bestSol[1])), str(bestSol))

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

if __name__ == '__main__':
    """
    PARAMS
    alpha:  relative importance of pheromone
    beta:   relative importance of heuristic information 
    sigma:  
    rho:    pheromone coefficient
    theta:
    num_ants:
    MAX_NFC: max number of function calls
    """

    vehicle_capacity, graph, delivery_demand, optimal = dataset('dataset.txt');

    alpha = 2
    beta = 5
    sigma = 3
    rho = 0.8
    theta = 80
    num_ants = 20
    MAX_NFC = 100

    vrp = ACOVRP( alpha, beta, sigma, rho, theta, num_ants, vehicle_capacity, delivery_demand, MAX_NFC )
    vrp.set_graph( graph )
    bestSol = vrp.process()
    
    if bestSol is not None:
        plot_paths( graph, bestSol )