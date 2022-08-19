

"""
Basic TSP Example
file: Individual.py
Author : Peter Sunny Shanthveer Markappa
Student Number : R00208303
"""

import random
import math

import random
import math

class Individual:
    def __init__(self, _size, _data, cgenes, _Initpop):
        """
        Parameters and general variables
        """
        self.initpop = _Initpop
        self.fitness    = 0
        self.genes      = []
        self.genSize    = _size
        self.data       = _data

        if self.initpop == 0:
           if cgenes: # Child genes from crossover
              self.genes = cgenes
           else:   # Random initialisation of genes
              self.genes = list(self.data.keys())
              random.shuffle(self.genes)
        elif self.initpop == 1:
           if cgenes:  # Child genes from crossover
              self.genes = cgenes
           else: #Nearest Neighbour
                Individual.nearestNeighbour(self)

    def setGenes(self, genes):
        self.genes = []
        for i in genes:
            self.genes.append(i)

    def geneSize(self, genSize):
        """ Updating Chromosome (Each Parent)"""
        self.genSize = genSize

    def nearestNeighbour(self):
        """ This code i have used  """
        unvisited = list(self.data.keys())
        tCost = 0

        # Randomly choose a city to start the tour
        cIndex = random.randint(0, len(self.data) - 1)
        # print(cIndex)
        tour = [unvisited[cIndex]]  # Initialise tour to this city
        del unvisited[cIndex]  # Remove from unvisited
        current_city = tour[0]  # This variable will store the last city added to the tour in each iteration
        while len(unvisited) > 0:
            # initialise the distance (bcost) to first unvisited city
            bCity = unvisited[0]
            bCost = self.euclideanDistance(current_city, bCity)
            bIndex = 0
            # Then iterate through remaining unvisited cities to see if there is a nearer city
            for city_index in range(1, len(unvisited)):
                city = unvisited[city_index]
                cost = self.euclideanDistance(current_city, city)

                if bCost > cost:
                    bCost = cost
                    bCity = city
                    bIndex = city_index
            tCost += bCost
            current_city = bCity
            tour.append(current_city)
            del unvisited[bIndex]

        tCost += self.euclideanDistance(tour[-1], tour[0])
        self.genes = tour
        self.fitness = tCost

    def copy(self):
        """
        Creating a copy of an individual
        """
        ind = Individual(self.genSize, self.data,self.genes[0:self.genSize], self.initpop)
        ind.fitness = self.getFitness()
        return ind

    def euclideanDistance(self, c1, c2):
        """
        Distance between two cities
        """
        d1 = self.data[c1]
        d2 = self.data[c2]
        return math.sqrt( (d1[0]-d2[0])**2 + (d1[1]-d2[1])**2 )

    def getFitness(self):
        return self.fitness

    def computeFitness(self):
        """
        Computing the cost or fitness of the individual
        """
        self.fitness    = self.euclideanDistance(self.genes[0], self.genes[len(self.genes)-1])
        for i in range(0, self.genSize-1):
            self.fitness += self.euclideanDistance(self.genes[i], self.genes[i+1])


