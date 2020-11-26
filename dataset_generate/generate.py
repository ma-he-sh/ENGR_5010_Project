import pandas as pd
import random as rand

max_capacity = 400 # fixed max capacity
min_demand   = 100  # min capacity

#vehical capcities
#capacity_arr = [ 1500, 2500, 2745, 4000, 11000, 15000 ] # capacity in pounds

# save the dataset
def save_template( filename, datafile, name, capacity, nodes, demands ):
    datalines = ("NAME : {name}\n"
    "CAPACITY : {capacity}\n"
    "DATAFILE : {datafile}\n"
    "NODE_COORD_SECTION\n"
    "{nodes}\n"
    "DEMAND_SECTION\n"
    "{demands}\n"
    "DEPOT_SECTION\n"
    "1\n"
    "-1\n"
    "EOF"
    ).format( datafile=datafile, name=name, capacity=capacity, nodes=nodes, demands=demands )
    f = open( "./datasets/" + filename, "w" )
    f.write( datalines )
    f.close()
    #print( "file saved", filename )

# get nodes
def get_data( list, max_demand, custCount=0 ):
    cordinate_file = "../helpers/raw_data/{filename}".format(filename=list['cordinates'])

    cordinate_data = pd.read_csv( cordinate_file )
    cordinates = cordinate_data.set_index( "x" )

    # to handle zero error on some distances, they are eliminated
    
    randomCitySample = rand.sample( cordinate_data['x'].tolist(), custCount )

    nodes = ""
    demands = ""
    index = 1
    for city in randomCitySample:
        row = cordinates.loc[city]
        nodes += "{index} {lat} {lng} {refid} {city}".format( index=index, lat=row['lat'], lng=row['lng'], refid=int(row['0']), city=city )
        
        capacity = int( abs( rand.random() * ( min_demand - max_demand ) ) )
        if index is 1:
            # index 1 is the store
            capacity = 0

        demands += "{index} {capacity} {refid} {city}".format( index=index, capacity=capacity, refid=int(row['0']), city=city )

        if len( randomCitySample ) != index:
            nodes += "\n"
            demands += "\n"

        index+=1

    return nodes, demands

if __name__ == '__main__':
    print('generate dataset')

    # raw data file list
    data_list = [{
        "fileID" : 1,
        "cordinates" : "cordinates_toronto.csv",
        "distances"  : "distance_toronto.csv",
        "customers": [ 23 ]
    }, {
        "fileID" : 2,
        "cordinates" : "cordinates_100.csv",
        "distances"  : "distance_100_cities.csv",
        "customers": [ 23, 50, 96 ]
    }, {
        "fileID" : 3,
        "cordinates" : "cordinates_250.csv",
        "distances"  : "distance_250_cities.csv",
        "customers": [ 23, 50, 96, 150, 200, 240 ]
    }]

    for list in data_list:
        for custCount in list.get('customers'):
            savefile = "data_{fileID}_{customers}".format( fileID=list['fileID'], customers=custCount )
            nodes, demands = get_data( list, max_capacity, custCount )
            save_template( savefile + ".txt", list["distances"], savefile, max_capacity, nodes, demands )