from functions import dataset
from SweepAlg import Sweep

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import random as rand

import time

if __name__ == '__main__':
    """
    """

    capacity, graph, delivery_demand, cityref, datafile = dataset('data_3_240.txt')

    for MAX_NFC in [ 200, 400, 1000, 2000 ]:
        sweep = Sweep( MAX_NFC )