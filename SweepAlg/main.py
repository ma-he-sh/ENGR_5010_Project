from functions import dataset
from sweep import Sweep

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import random as rand

import functions as dataset
import time

if __name__ == '__main__':
    """
    capacity : capacity
    graph    : Graph
    delivery_demand : Delivery demands
    """

    capacity, graph, delivery_demand, cityref, datafile = dataset('data_3_240.txt')
    
    #-------------------------
    tempdata = pd.read_csv("data_2_23.txt")
    citydata = tempdata.set_index("x")

    sweepAlg = Sweep( capacity, delivery_demand, cityref, citydata )
    sweepAlg.init_customers()

    start_time = time.time()
    bestSol = sweepAlg.process()
    elasped_time = (time.time() - start_time )
    
    if bestSol is not None:
        print( bestSol )
