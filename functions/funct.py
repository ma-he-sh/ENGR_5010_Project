import requests
from dotenv import load_dotenv
from pathlib import Path
import json
import os

env_path = Path(".") / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

# get distance between two points in meters
def getDistance( start_loc, end_loc ):
    apiKEY = os.getenv( "GOOGLE_MAP_KEY" )
    reqURL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={start}&destinations={end}&key={apikey}".format( start=start_loc, end=end_loc, apikey=apiKEY )
    request= requests.get( reqURL )
    response = request.json()

    distance = None
    if 200 is request.status_code:
        distance = response['rows'][0]['elements'][0]['distance']['value']
    
    return distance

# TEST
dist = getDistance( 'Toronto, ON, Canada', 'Oshawa, ON, Canada' )
print( dist )