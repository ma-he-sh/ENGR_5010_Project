from functions.funct import preCompile, saveCSV
import numpy as np

if __name__ == "__main__":
    # TEST
    #dist = getDistance( 'Toronto, ON, Canada', 'Oshawa, ON, Canada' )
    #print( dist )

    list = preCompile()
    saveCSV(list)