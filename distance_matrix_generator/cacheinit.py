from functions.funct import createInitCache, saveCSV, GetEnv
import numpy as np

if __name__ == "__main__":
    list = createInitCache()
    print( "CACHE INIT DISABLED TO SAVE REQUESTS, uncomment saveCSV" )
    #saveCSV( GetEnv('CACHE_DATA'), list)