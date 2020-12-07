from ast import literal_eval
from functions import dataset
import numpy as np
import pandas as pd
import random as rand

import matplotlib.pyplot as plt

bestSol = "[[138, 8, 38, 7, 77, 16, 75, 27, 20, 5, 184, 227, 192, 195], [226, 176, 173, 198, 100, 17, 44, 179, 83, 182, 14, 194], [223, 72, 235, 22, 240, 144, 139, 3, 172, 207, 71, 37], [40, 63, 211, 36, 218, 120, 60, 106, 129, 47], [191, 157, 105, 201, 35, 197, 224, 43, 19], [113, 146, 239, 233, 116, 31, 238, 219, 9, 4, 150, 6, 185], [229, 154, 115, 48, 161, 64, 168, 234, 33, 237], [57, 148, 147, 13, 82, 91, 199, 97, 111, 23, 190, 162, 53], [65, 189, 202, 114, 41, 153, 221, 11, 25, 135, 204, 118, 136], [126, 70, 78, 169, 232, 127, 159, 46, 231, 67], [203, 205, 85, 10, 76, 225, 142, 187, 152, 12, 196], [156, 109, 28, 94, 130, 30, 177, 49, 220], [149, 79, 183, 104, 228, 69, 217, 73, 222, 151, 145, 80, 206, 236, 51], [163, 141, 132, 180, 93, 32, 110, 92, 21, 58, 164, 55], [99, 208, 45, 181, 143, 123, 66, 117, 175, 59, 124], [121, 81, 125, 88, 213, 155, 212, 133, 50, 96, 26], [86, 2, 119, 134, 178, 87, 108, 214, 84, 90, 103], [68, 42, 24, 200, 56, 39, 137, 171, 186, 52], [15, 101, 209, 170, 174, 29, 54, 62, 193, 160, 165, 166, 210], [140, 216, 131, 230, 167, 95, 18, 102, 107], [61, 112, 74, 89, 34, 158, 215, 128, 188, 122, 98]]"

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