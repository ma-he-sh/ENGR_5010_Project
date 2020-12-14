import numpy as np
from functions import dataset
from functools import reduce
import random as rand 

class Sweep():
    def __init__( self, MAX_NFC ):
        print( "sweep algorithm" )
        self.MAX_NFC = MAX_NFC
    
    def process(self):
        NFC = 0
        bestSol = None

        while( NFC < self.MAX_NFC ):


            NFC += 1
        return bestSol