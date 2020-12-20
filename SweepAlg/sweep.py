import numpy as np
import random as rand
import math as mt

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

class Customer:
    def __init__(self, location, posX, posY, demand ):
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

    def getDepotAngle(self):
        return self.angle

class TSP:
    def __init__(self, num_customers, num_vehicles, depot_index ):
        self.num_customer  = num_customers
        self.num_vehicles = num_vehicles
        self.depot_index   = depot_index

    def get_city_distances(self, cityIndex1, cityIndex2):
        """
        Get distance with distance matrix
        """
        distance = self.citydata.loc[cityIndex1][cityIndex2]
        return distance

    def get_routes(self):
        routes = []
        if self.num_customers > 0:
            print("num customers", self.num_customers )

            # Create the routing index manager
            manager = pywrapcp.RoutingIndexManager(self.num_customers, self.num_vehicles, self.depot_index )

            # Create Routing Model
            routing = pywrapcp.RoutingModel( manager )

            # Create and register a transit callback
            def distance_callback(from_index, to_index):
                return 1

            # Define cost of each arc
            transient_callback_index = routing.RegisterTransitCallback( distance_callback )
            routing.SetArcCostEvaluatorOfAllVehicales( transit_callback_index )

            # Settings first solution heuristic
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

            solution = routing.SolveWithParameters( search_parameters )
            if solution:
                routeNode = routing.Start( self.depot_index )
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
            #print( self.graph[i][0], self.cityref[i], self.delivery_demand[i])
            demand = self.delivery_demand[i]
            cust = Customer( self.cityref[i], float(self.graph[i][0]), float(self.graph[i][1]), int(demand) )
            CustomerList.append( cust )

        depot = CustomerList[0]  # set the depot
        for custInd in range(1, len(self.CustomerList)):
            #print( CustomerList[custInd].location )
            CustomerList[custInd].calc_city_angle( depot.posX, depot.posY )
            #print( CustomerList[custInd].angle )

        CustomerList.sort(key=lambda cust:cust.angle, reverse=False)
        self.CustomerList = CustomerList

    def init_customers(self):
        return 1

    def process(self):
        print( self.CustomerList )
        bestSol = None

