from acovrp import ACOVRP
from functions import dataset

if __name__ == '__main__':
    """
    PARAMS
    alpha:  relative importance of pheromone
    beta:   relative importance of heuristic information 
    sigma:  
    rho:    pheromone cofficient
    theta:
    num_ants:
    MAX_NFC: max number of function calls
    """

    vehicle_capacity, graph, delivery_demand, optimal = dataset('dataset.txt');

    alpha = 2
    beta = 5
    sigma = 3
    rho = 0.8
    theta = 80
    num_ants = 20
    MAX_NFC = 10

    vrp = ACOVRP( alpha, beta, sigma, rho, theta, num_ants, vehicle_capacity, delivery_demand, MAX_NFC )
    vrp.set_graph( graph )
    bestSol = vrp.process()
    print( "best solution:", str( int(bestSol[1]) ), str( bestSol ) )