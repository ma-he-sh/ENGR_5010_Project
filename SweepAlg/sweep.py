import numpy as np
import random as rand
import math as mt
import copy

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

class Customer:
    def __init__(self, index, location, posX, posY, demand ):
        self.index    = index
        self.location = location
        self.demand   = demand
        self.posX     = posX
        self.posY     = posY
        self.angle    = 0

    def calc_city_angle(self, depotX, depotY):
        """
        Get angle from the depot to ref city using slope
        """
        opposite = ( self.posX - depotX )
        adjacent = ( self.posY - depotY )
        angle = mt.degrees(mt.atan( opposite / adjacent ))
        self.angle = ( 90 - angle ) % 360

class TSP:
    def __init__(self, num_customers, num_vehicles, depot_index ):
        self.num_customers   = num_customers
        self.num_vehicles   = num_vehicles
        self.depot_index    = depot_index
    
    def get_routes(self, cluster, citydata ):
        routes = []
        if self.num_customers > 0:
            # Create the routing index manager
            manager = pywrapcp.RoutingIndexManager(self.num_customers, self.num_vehicles, self.depot_index )

            # Create Routing Model
            routing = pywrapcp.RoutingModel( manager )

            def get_distance_callback( clustIndex1, clustIndex2 ):
                """
                get distance with distance matrix
                """
                cityIndex1 = cluster[clustIndex1].location
                cityIndex2 = cluster[clustIndex2].location

                distance = float(citydata.loc[cityIndex1][cityIndex2])
                #print( "city distance", cityIndex1, cityIndex2, distance )

                return distance

            # Define cost of each arc
            transit_callback_index = routing.RegisterTransitCallback( get_distance_callback )
            routing.SetArcCostEvaluatorOfAllVehicles( transit_callback_index )

            # Settings first solution heuristic
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

            solution = routing.SolveWithParameters( search_parameters )
            if solution:
                routeNode = routing.Start( 0 )
                while not routing.IsEnd( routeNode ):
                    routes.append( routeNode )
                    routeNode = solution.Value( routing.NextVar( routeNode ) )
                routes.append( self.depot_index )
            else:
                return -1
        return routes

class Sweep:
    graph = {}

    def __init__( self, vehicle_capacity, delivery_demand, cityref, citydata ):
        print( "sweep algorithm" )
        self.cityref      = cityref
        self.vehicle_capacity = vehicle_capacity
        self.delivery_demand   = delivery_demand
        self.cityref          = cityref
        self.citydata         = citydata
        self.CustomerList = []

    def set_graph(self, graph):
        self.graph = graph
        CustomerList = []

        for i in self.graph.keys():
            demand = 0
            #print( i, self.graph[i][0], self.cityref[i], self.delivery_demand[i])
            demand = self.delivery_demand[i]
            cust = Customer( i, self.cityref[i], float(self.graph[i][0]), float(self.graph[i][1]), int(demand) )
            CustomerList.append( cust )

        depot = CustomerList[0]  # set the depot
        for custInd in range(1, len(self.CustomerList)):
            #print( CustomerList[custInd].location )
            CustomerList[custInd].calc_city_angle( depot.posX, depot.posY )
            #print( CustomerList[custInd].angle )

        CustomerList.sort(key=lambda cust:cust.angle, reverse=False)
        self.CustomerList = CustomerList

    def get_cluster(self):
        cluster = []
        tmpCluster = []

        depot = self.CustomerList[0]
        self.CustomerList.pop(0)

        deepCustomer = copy.deepcopy( self.CustomerList )
        currCapacity = 0

        while len(deepCustomer):
            cust = deepCustomer.pop(0)
            #print(cust)

            if currCapacity + cust.demand <= self.vehicle_capacity:
                tmpCluster.append( cust )
                currCapacity += cust.demand
            else:
                cluster.append(tmpCluster)
                tmpCluster = []
                tmpCluster.append(cust)
                currCapacity = cust.demand
        cluster.append(tmpCluster)
        return cluster, depot

    def process(self):
        bestSol = []
        cluster, depot = self.get_cluster()
        #print(len(cluster), cluster, depot, depot.index )

        for path in cluster:
            path.insert(0, depot)

            tsp = TSP( len(path), 1, depot.index )
            route = tsp.get_routes( path, self.citydata )
            bestSol.append( route )


        return bestSol
