import numpy as np
from functions import dataset
from functools import reduce

import random as rand
import copy

class Ant():
    startPoint = 1

    vertices = list()
    edges    = {}
    pheromones = {}
    maxCapacity = 0
    demand   = 0

    alpha = 0
    beta  = 0

    solution = list()

    def __init__(self, vertices, edges, maxCapacity, demand, pheromones, alpha, beta, startPoint=1 ):
        self.startPoint = startPoint
        self.vertices = vertices
        self.edges = edges
        self.maxCapacity = maxCapacity
        self.demand = demand
        self.pheromones = pheromones
        self.alpha = alpha
        self.beta  = beta
        self.solution = list()
        
    def set_state_transition(self):
        """
        State transition
        """
        while( len( self.vertices ) is not 0 ):
            path =  list()
            city = rand.choice( self.vertices ) #np.random.choice(self.vertices)
            capacity = self.maxCapacity - self.demand[ city ]
            
            path.append( city )
            self.vertices.remove( city )

            while( len( self.vertices ) is not 0 ):
                prob = list()
                for x in self.vertices:
                    p = ((self.pheromones[(min(x, city), max(x, city))]) ** self.alpha) * ((1 / self.edges[(min(x, city), max(x, city))] if self.edges[(min(x, city), max(x, city))] else 0 ) ** self.beta)
                    prob.append(p)
                
                probability = (prob / np.sum( prob ) if np.sum( prob ) else [1] )

                city = np.random.choice( self.vertices, p=probability )
                capacity = capacity - self.demand[city]

                if capacity>0:
                    path.append(city)
                    self.vertices.remove(city)
                else:
                    break
            self.solution.append( path )
        return self.solution

    def get_solution(self):
        """
        get solution
        """
        solution = 0
        for i in self.solution:
            a = self.startPoint
            for j in i:
                b = j
                solution = solution + self.edges[(min(a, b), max(a, b))]
                a = b
            b = 1
            solution = solution + self.edges[(min(a, b), max(a, b))]
        return solution

class ACOVRP():
    alpha = 2
    beta  = 5
    sigma = 3
    rho   = 0.8
    theta = 80
    num_ants = 2
    vehicle_capacity = 0
    delivery_demand = {}
    cityref = {}
    MAX_NFC  = 1000

    graph = {}

    def __init__(self, alpha, beta, sigma, rho, theta, num_ants, vehicle_capacity, delivery_demand, cityref, citydata, MAX_NFC):
        self.MAX_NFC = MAX_NFC
        self.num_ants = num_ants
        self.theta = theta
        self.rho = rho
        self.sigma = sigma
        self.beta = beta
        self.alpha = alpha
        self.vehicle_capacity = vehicle_capacity
        self.delivery_demand = delivery_demand
        self.cityref = cityref

        print("----------------")
        print( "alpha: ", self.alpha, " beta: ", self.beta, " sigma: ", self.sigma, " rho: ", self.rho, " theta: ", self.theta, " ants: ", self.num_ants, " max_nfc: ", self.MAX_NFC, " max_vehicle_cap: ", self.vehicle_capacity )
        print("----------------")

        self.citydata = citydata
        self.bestSolTemp = []

    def get_city_distance(self, cityIndex1, cityIndex2 ):
        """
        Euclidean distance calculate
        """
        distance = self.citydata.loc[cityIndex1][cityIndex2]
        return distance

    def set_graph( self, graph ):
        self.graph = graph

    def prepare_graph(self ):
        vertices = list( self.graph.keys() )
        vertices.remove(1) # use 1 as deport

        edges = {}
        for pointA in self.graph.keys():
            for pointB in self.graph.keys():
                edges[(pointA, pointB)] = int(self.get_city_distance( self.cityref[pointA], self.cityref[pointB] ))

        return vertices, edges

    def init_pheromone(self):
        pheromones = {}
        for p in self.graph.keys():
            for q in self.graph.keys():
                pheromones[(p, q)] = 1

        return pheromones

    def sort_list(self, x):
        return x[1]

    def update_global_pheromone(self, sols, pheromones, bestSol ):
        """
        Update pheromones
        """
        sum = 0
        for i in sols:
            sum += i[1]
        avgSol = sum / len( sols )

        newPheromones = {}
        for ( key, value ) in pheromones.items():
            newPheromones[key] = ( self.rho + self.theta / avgSol ) * value

        sols.sort( key=self.sort_list )

        if bestSol is not None:
            if sols[0][1] <  bestSol[1]:
                bestSol = sols[0]
            
            for path in bestSol[0]:
                for i in range( len( path ) - 1 ):
                    newPheromones[ ( min( path[i], path[i+1] ), max( path[i], path[i+1] ) ) ] = self.sigma / bestSol[1] + newPheromones[ min( path[i], path[i + 1] ), max( path[i], path[i + 1] ) ]
        else:
            bestSol = sols[0]

        for l in range(self.sigma):
            paths = sols[l][0]
            L = sols[l][1]
            for path in paths:
                for i in range(len(path)-1):
                    newPheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = (self.sigma-(l+1)/L**(l+1)) + newPheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]

        return bestSol

    def get_cost_from_depot( self ):
        bestSol = []

        paths   = []
        cost    = 0
        for pathSol in self.bestSolTemp:
            # add depot
            pathSol.insert(0, 1)
            pathSol.append(1)
            paths.append( pathSol )

            for i in range( len( pathSol ) - 1 ):
                cost += int( self.get_city_distance( self.cityref[pathSol[i]], self.cityref[pathSol[i+1]] ) )

        bestSol.append( paths )
        bestSol.append( cost )
        return bestSol

    def process(self):
        vertices, edges = self.prepare_graph()
        pheromones = self.init_pheromone()

        NFC = 0
        bestSol = None

        while( NFC < self.MAX_NFC ):
            sols = list()
            # run per each ant
            for i in range(self.num_ants):
                ant = Ant( vertices.copy(), edges, self.vehicle_capacity, self.delivery_demand, pheromones, self.alpha, self.beta )
                solution = ant.set_state_transition()
                rate = ant.get_solution()
                sols.append((solution, rate))
            bestSol = self.update_global_pheromone( sols, pheromones, bestSol )
            #print( "generation:", NFC, " best:", int(bestSol[1]), " path:", str( bestSol[0] ) )
            NFC += 1

        self.bestSolTemp = copy.deepcopy(bestSol[0])
        return bestSol