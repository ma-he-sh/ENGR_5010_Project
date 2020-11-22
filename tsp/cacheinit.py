from functions.funct import createInitCache, saveCSV, GetEnv
import numpy as np

if __name__ == "__main__":
    list = createInitCache()
    saveCSV( GetEnv('CACHE_DATA'), list)