import json
import pandas as pd

from functions import dataset

if __name__ == '__main__':
	dataset_name = "data_3_96"
	capacity, graph, delivery_demand, cityref, indexes, datafile = dataset( dataset_name + '.txt')

	data_arr = {}
	for i in graph:
		data_arr[i] = {
			"index" : int(i),
			"location": cityref[i],
			"lat" : float(graph[i][0]),
			"lng" : float(graph[i][1]),
			"demand" : float(delivery_demand[i]),
			"cityref": int(indexes[i]),
		}

	jsonData = json.dumps(data_arr, indent=4)

	with open( "./dataset/" + dataset_name + ".json", "w" ) as f:
		f.write( jsonData )