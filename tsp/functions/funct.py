import requests
from dotenv import load_dotenv
from pathlib import Path
import json
import os
import numpy as np
import time
import pandas as pd
import random

env_path = Path(".") / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

def GetEnv( key ):
    return os.getenv(key)

# get distance between two points in meters
def getDistance( start_loc, end_loc ):
    time.sleep(.01)
    apiKEY = os.getenv( "GOOGLE_MAP_KEY" )
    reqURL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={start}&destinations={end}&key={apikey}".format( start=start_loc, end=end_loc, apikey=apiKEY )
    request= requests.get( reqURL )
    response = request.json()

    print( response )

    distance = '-'
    if 200 is request.status_code:
        print( response['status'] )
        if response['status'] == "OVER_QUERY_LIMIT":
            time.sleep(2)

        if 'REQUEST_DENIED' is not response['status']:
            if( response['rows'][0]['elements'][0]['status'] == 'OK' ):
                distance = response['rows'][0]['elements'][0]['distance']['value']
            else:
                distance = 'ZERO'
    return distance

# get distance while checking cache exists
def getDistanceBetweenTwoCities( start_loc, end_loc ):
    if start_loc.get('city') == end_loc.get('city'):
        return 0

    df = pd.read_csv( os.getenv('CACHE_DATA') )
    data = df.set_index('x')
    distance = data.at[start_loc.get('city'), end_loc.get('city')]
    if distance == '-':
        distance = getDistance( start_loc.get('address'), end_loc.get('address') )
        data.at[start_loc.get('city'), end_loc.get('city')] = distance
        data.to_csv( os.getenv('CACHE_DATA'), header=True, index=True )

    return distance

# get city list
def getCityList(Province='Ontario'):
    dataList = []
    cityList = []
    file = open( os.getenv("CITY_LIST"), "r" )

    tempList = []

    while True:
        line = file.readline()
        address = line.strip()
        parts= address.split(", ")
        if len(parts) >= 2 and Province == parts[1]:
            tempList.append( address )

        if not line:
            break

    randomList = tempList
    for line in randomList:
        address = line.strip()
        parts = address.split(", ")
        if len(parts) >= 2 and Province == parts[1]:
            cityList.append(parts[0])
            dataList.append({
                'city': parts[0],
                'province': parts[1],
                'address': address
            })

    file.close()
    return dataList, cityList

# create initial file cache
def createInitCache(Province='Ontario'):
    dataList, cityList = getCityList(Province)

    dataMatrix = [[0 for j in range(len( cityList ) + 1)] for i in range(len( cityList ) + 1)]
    dataMatrix[0][0] = "x"
    for i in range( len(cityList) ):
        dataMatrix[i+1][0] = cityList[i]
        dataMatrix[0][i+1] = cityList[i]

    # 705600

    seen=set()
    seenDistance={}
    for i in range( len( dataList ) ):
        for j in range( len( dataList ) ):
            fromLoc = dataList[i].get('address')
            toLoc   = dataList[j].get('address')

            t1 = tuple( [ fromLoc, toLoc ] )
            t2 = tuple( [ toLoc, fromLoc ] )

            if t1 not in seen and t2 not in seen:
                if fromLoc == toLoc:
                    """
                    distance to itself would be 0
                    """
                    distance = 0
                else:
                    distance = '-'

                dataMatrix[i + 1][j + 1] = distance

                # save distance for reference
                seenDistance[ fromLoc+toLoc ] = distance
                seenDistance[ toLoc+fromLoc ] = distance
                
                seen.add(t1)
                seen.add(t2)
            else:
                dataMatrix[i + 1][j + 1] = seenDistance[ fromLoc+toLoc ]
    return dataMatrix

# pre set distances :: through google
def preCompile(Province='Ontario'):
    REQCOUNT = 0
    dataList, cityList = getCityList(Province)

    dataMatrix = [[0 for j in range(len( cityList ) + 1)] for i in range(len( cityList ) + 1)]
    dataMatrix[0][0] = "x"
    for i in range( len(cityList) ):
        dataMatrix[i+1][0] = cityList[i]
        dataMatrix[0][i+1] = cityList[i]

    # 705600

    restMade = True
    seen=set()
    seenDistance={}
    for i in range( len( dataList ) ):
        for j in range( len( dataList ) ):
            fromLoc = dataList[i].get('address')
            toLoc   = dataList[j].get('address')

            t1 = tuple( [ fromLoc, toLoc ] )
            t2 = tuple( [ toLoc, fromLoc ] )

            if t1 not in seen and t2 not in seen:
                if fromLoc == toLoc:
                    """
                    distance to itself would be 0
                    """
                    distance = 0
                    restMade = False
                else:
                    # if restMade:
                    #     time.sleep(.10)
                    
                    #distance = getDistance( fromLoc, toLoc )
                    distance = 'req'
                    restMade=True
                    REQCOUNT += 1

                dataMatrix[i + 1][j + 1] = distance

                # save distance for reference
                seenDistance[ fromLoc+toLoc ] = distance
                seenDistance[ toLoc+fromLoc ] = distance
                
                seen.add(t1)
                seen.add(t2)
                print('not seen')
            else:
                dataMatrix[i + 1][j + 1] = seenDistance[ fromLoc+toLoc ]
                print('seen')

    print( "REQ COUNT", REQCOUNT )

    return dataMatrix

def saveCSV( fileName, list ):
    a = np.asarray( list )
    np.savetxt( fileName , a, delimiter=",", fmt='%s')


def savePDCSV( df ):
    df.to_csv( os.getenv("SAVE_DATA"), header=False, index=True )