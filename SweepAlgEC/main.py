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

    vehicle_capacity, graph, delivery_demand, optimal = dataset('dataset.txt')
    
    sweepAlg = Sweep( vehicle_capacity, delivery_demand )
    start_time = time.time()
    sweepAlg.set_graph( graph )
    bestSol = sweepAlg.process()
    elasped_time = (time.time() - start_time )

    if bestSol is not None:
        plot_paths( graph, bestSol )
