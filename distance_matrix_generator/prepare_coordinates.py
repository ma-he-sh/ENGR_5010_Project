from functions.funct import getCityListFromFile, getCordinates, savePDTOCSV
import pandas as pd

"""
            xmin      ymin      xmax    ymax
 Ontario  |  -95.16 | 41.66 |  -74.34 | 56.86
"""

if __name__ == '__main__':
    print( "Get City list from file" )
    cityList = getCityListFromFile("functions/distance_toronto.csv")
    
    list = []
    list.append( {
        'city': 'x',
        'lat' : 'lat',
        'lng' : 'lng',
    } )

    if len(cityList) > 0:
        for cityObj in cityList:
            print( cityObj['city'] )
            coo = getCordinates( cityObj['address'], cityObj['city'] )
            list.append( coo )

        df = pd.DataFrame(list)
        savePDTOCSV( df, 'functions/cordinates_toronto.csv' )
