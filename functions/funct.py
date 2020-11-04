import requests
from dotenv import load_dotenv
from pathlib import Path
import json
import os
import numpy as np
import time

env_path = Path(".") / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

# get distance between two points in meters
def getDistance( start_loc, end_loc ):
    apiKEY = os.getenv( "GOOGLE_MAP_KEY" )
    reqURL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={start}&destinations={end}&key={apikey}".format( start=start_loc, end=end_loc, apikey=apiKEY )
    request= requests.get( reqURL )
    response = request.json()

    distance = '-'
    if 200 is request.status_code:
        distance = response['rows'][0]['elements'][0]['distance']['value']
    
    return distance

# pre set distances
def preCompile(Province='Ontario'):
    """
    Np : number of cities
    """
    dataList = []
    cityList = []
    file = open( os.getenv("CITY_LIST"), "r" )

    REQCOUNT = 0

    while True:
        line = file.readline()
        address = line.strip()
        parts= address.split(", ")
        if len(parts) >= 2 and Province == parts[1]:
            cityList.append( parts[0] )
            dataList.append( {
                'city':parts[0],
                'province': parts[1],
                'address' : address
            } )

        if not line:
            break

    file.close()

    dataMatrix = [[0 for j in range(len( cityList ) + 1)] for i in range(len( cityList ) + 1)]
    dataMatrix[0][0] = ""
    for i in range( len(cityList) ):
        dataMatrix[i+1][0] = cityList[i]

    # 705600

    for i in range( len( dataList ) ):
        for j in range( len( dataList ) ):
            fromLoc = dataList[i].get('address')
            toLoc   = dataList[j].get('address')
            distance = getDistance( fromLoc, toLoc )
            dataMatrix[i + 1][j + 1] = distance
            REQCOUNT += 1
            print( REQCOUNT , distance )
            time.sleep(.200)

    return dataMatrix

def saveCSV( list ):
    a = np.asarray( list )
    np.savetxt( os.getenv("SAVE_DATA") , a, delimiter=",", fmt='%s')