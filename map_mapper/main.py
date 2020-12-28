from ast import literal_eval
from functions import dataset
import numpy as np
import pandas as pd
import random as rand

import matplotlib.pyplot as plt

bestSol = "[[13, 11, 2, 6, 4, 9, 3, 16, 7, 8, 5, 12, 10, 14, 15], [25, 21, 26, 23, 19, 24, 27, 20, 18, 28, 22], [33, 36, 34, 32, 37, 31, 30, 35, 38], [40, 47, 46, 45, 42, 43, 41, 44], [55, 58, 50, 57, 53, 52, 54, 51, 49, 56], [64, 63, 60, 67, 61, 66, 68, 62, 69, 65], [74, 78, 71, 72, 73, 79, 76, 80, 75, 77], [85, 83, 86, 87, 84, 90, 91, 82, 89, 88], [103, 97, 93, 98, 96, 99, 102, 95, 94, 100, 101], [106, 107, 112, 110, 111, 108, 105, 109, 113, 114], [120, 118, 127, 126, 116, 119, 124, 117, 123, 125, 121, 122], [133, 132, 129, 135, 136, 134, 139, 130, 137, 131, 138], [141, 148, 147, 146, 144, 143, 145, 142], [154, 153, 150, 151, 152, 157, 156, 155, 158], [161, 168, 166, 165, 164, 163, 169, 162, 172, 171, 167, 160, 170], [176, 179, 182, 174, 183, 187, 177, 181, 184, 175, 186, 185, 178, 180], [190, 189, 192, 195, 191, 197, 196, 193, 194], [204, 202, 209, 205, 203, 206, 201, 200, 208, 207, 199], [211, 213, 212, 215, 218, 221, 214, 219, 223, 217, 222, 220, 216], [229, 234, 231, 232, 227, 230, 235, 233, 226, 228, 225], [237, 239, 238]]"

capacity, graph, delivery_demand, cityref, datafile = dataset( "data_3_240.txt" )
tempdata = pd.read_csv("../helpers/raw_data/" + datafile )


def plot_paths( graph, cityref, bestSol, plot=True ):

    if plot:
        # deport location
        deportX, deportY = graph.get(1)

        for i in range(0, len(bestSol)):
            points = {
                "x": [],
                "y": []
            }

            # start point
            points["x"].append(deportX)
            points["y"].append(deportY)

            for j in range(0, len(bestSol[i]) - 1):
                pathFrom = bestSol[i][j]
                pathTo = bestSol[i][j + 1]

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

            plt.plot(points["x"], points["y"], marker='o', linestyle="--")

        # draw labels
        for city in graph:
            label = cityref[city]
            plt.annotate( cityref[city], graph[city], textcoords="offset points", xytext=(0, 10), ha="center", fontsize=6 )

        # img = plt.imread("./ontario_map.jpg")
        # fig, ax = plt.subplots()
        # ax.imshow(img)

        plt.plot(deportX, deportY, marker='x')
        plt.title('Paths')
        plt.show()


if __name__ == "__main__":
    data = literal_eval(  bestSol )
    plot_paths( graph, cityref, data, True )