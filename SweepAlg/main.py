from functions import dataset, plot_paths
from sweep import Sweep

import numpy as np
import pandas as pd
import random as rand
import time

if __name__ == '__main__':
    """
    capacity : capacity
    graph    : Graph
    delivery_demand : Delivery demands
    """

    capacity, graph, delivery_demand, cityref, datafile = dataset('data_3_240.txt')

    #-------------------------
    tempdata = pd.read_csv( "../helpers/raw_data/" + datafile )
    citydata = tempdata.set_index("x")
    
    for vehicle_capacity in [1000, 1500, 2500, 2000, 2745, 4000, 11000, 15000]:
        sweepAlg = Sweep( vehicle_capacity, delivery_demand, cityref, citydata )

        start_time = time.time()
        sweepAlg.set_graph( graph )
        bestSol = sweepAlg.process()
        elasped_time = (time.time() - start_time )

        if bestSol is not None:
            plot_paths( graph, cityref, bestSol, elasped_time, False )
