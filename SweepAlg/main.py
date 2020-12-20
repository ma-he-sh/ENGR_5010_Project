from functions import dataset
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

    capacity, graph, delivery_demand, cityref, datafile = dataset('data_1_23.txt')

    #-------------------------
    tempdata = pd.read_csv( "../helpers/raw_data/" + datafile )
    citydata = tempdata.set_index("x")

    capacity = 2000



    sweepAlg = Sweep( capacity, delivery_demand, cityref, citydata )
    sweepAlg.set_graph( graph )

    start_time = time.time()
    bestSol = sweepAlg.process()
    elasped_time = (time.time() - start_time )
    
    if bestSol is not None:
        print( bestSol )
