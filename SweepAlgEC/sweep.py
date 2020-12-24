import numpy as np
import random as rand
import math as mt
import copy

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

class Customer:
    def __init__(self, index, posX, posY, demand ):
        self.index    = index
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
   
    def get_distance( self, x1, x2, y1, y2 ):
        """
        Get matrix distance
        """
        return np.sqrt( ( x1 - x2 ) ** 2 + ( y1 - y2 ) ** 2 )

    def prepare_path(self, cluster ):
        routes = []
        if self.num_customers > 0:
            # Create the routing index manager
            manager = pywrapcp.RoutingIndexManager(self.num_customers, self.num_vehicles, self.depot_index )

            # Create Routing Model
            routing = pywrapcp.RoutingModel( manager )


            def get_distance_callback( clustIndex1, clustIndex2 ):
                """
                get euclidean distance
                """

                x1 = int(cluster[clustIndex1].posX)
                y1 = int(cluster[clustIndex1].posY)

                x2 = int(cluster[clustIndex2].posX)
                y2 = int(cluster[clustIndex2].posY)

                return self.get_distance( x1, x2, y1, y2 )
                

            # Define cost of each arc
            transit_callback_index = routing.RegisterTransitCallback( get_distance_callback )
            routing.SetArcCostEvaluatorOfAllVehicles( transit_callback_index )

            # Settings first solution heuristic
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

            solution = routing.SolveWithParameters( search_parameters )
            if solution:
                route = ''
                routeNode = routing.Start( self.depot_index )
                while not routing.IsEnd( routeNode ):
                    routes.append( routeNode )
                    routeNode = solution.Value( routing.NextVar( routeNode ) )
            else:
                return -1
        return routes

    def get_routes(self, cluster ):
        paths    = []
        cost    = 0
        routes = self.prepare_path( cluster )
        if len(routes) > 0:
            for path in routes:
                if path != 0: 
                    # ignore depot which is on index 1
                    paths.append( cluster[path].index )

            routes.append(0)
            for i in range(len(routes) - 1):
                pathCurr = routes[i]
                pathNext = routes[i+1]
                cost += self.get_distance( cluster[pathCurr].posX, cluster[pathNext].posX, cluster[pathCurr].posY, cluster[pathNext].posY )

        return paths, cost

class Sweep:
    graph = {}

    def __init__( self, vehicle_capacity, delivery_demand ):
        #print( "sweep algorithm" )
        self.vehicle_capacity = vehicle_capacity
        self.delivery_demand   = delivery_demand
        self.CustomerList = []

        print("-------------------")
        print(" max_vehicle_cap: ", vehicle_capacity )
        print("-------------------")

    def set_graph(self, graph):
        self.graph = graph
        CustomerList = []

        for i in self.graph.keys():
            demand = 0
            demand = self.delivery_demand[i]
            cust = Customer( i, float(self.graph[i][0]), float(self.graph[i][1]), int(demand) )
            CustomerList.append( cust )

        depot = CustomerList[0]  # set the depot
        for custInd in range(1, len(self.CustomerList)):
            CustomerList[custInd].calc_city_angle( depot.posX, depot.posY )

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
        cluster, depot = self.get_cluster()
        #print(len(cluster), cluster, depot, depot.index )
        bestSol = list()

        sols = []
        pathCost = 0
        for path in cluster:
            path.insert(0, depot)

            # for i in range(len(path)): 
            #     print (i, end = " ") 
            #     print (path[i]) 

            tsp = TSP( len(path) - 1, 1, 0 )
            route, cost = tsp.get_routes( path )
            pathCost += cost
            sols.append( route )
        
        bestSol.append( sols  )
        bestSol.append( pathCost )

        return bestSol 
