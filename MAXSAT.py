

"""
''' 
Name : Peter Sunny Shanthveer Markappa
Student Number: R00208303
Subject: Meta-Heuristic Optimisation
Data of Submission: 14-August-2022
Task: Genetic Algorithm using MAxWeight
'''

"""

import random
import secrets
from turtle import clear
# from Individual import *
import sys
import numpy as np
import time


myStudentNum = 208303 # Replace 12345 with your student number
random.seed(myStudentNum)


class Individual:
    def __init__(self, _data, cgenes, heuristic=0, individual_no=0):
        """
        Parameters and general variables
        """
        self.weight = 0
        self.genes = []
        self.data = _data
        self.heuristic = heuristic
        self.individual_no = individual_no
        self.truth_false_assignment = []

        if cgenes:  # Child genes from crossover
            self.truth_false_assignment = cgenes
            self.genes = np.array(self.data[0]) * cgenes
        else:
            if self.heuristic == 0:
                # Random initialisation of genes
                self.genes = self.data[0].copy()
                # # Randomly flip the bits in the genes
                random.seed(self.individual_no + myStudentNum)
                no_of_ones = random.randint(0, len(self.genes) - 1)

                # Here I'm considering 1 and -1 instead of 0, to reduce the computation
                # but while printing will print in format of 1 and 0
                ones = [1] * no_of_ones
                negative_ones = [-1] * (len(self.genes) - no_of_ones)
                random_list = ones + negative_ones
                random.shuffle(random_list)
                self.truth_false_assignment = random_list

                self.genes = np.array(self.data[0]) * np.array(random_list)
                print("Genes Assigned")
                print(self.genes)
            else:
                print("Select 0 for random initialisation")
                sys.exit(0)

    def copy(self):
        """
        Creating a copy of an individual
        """
        ind = Individual(self.data, self.truth_false_assignment, self.heuristic)
        ind.computeweight()
        ind.fitness = self.getWeight()
        return ind

    def computeweight(self):
        'Calculates Weight for the individual i.e Fitness score'

        unsatClause = []
        weight = 0
        j = 0
        for clause_ in self.data[1]:
            if len(set(clause_) & set(self.genes)) == 0:
                unsatClause.append(clause_)
                clause_weight = 0
            else:
                clause_weight = self.data[2][j]
            self.weight += clause_weight

            j += 1

    def getWeight(self):
        return self.weight


class GeniticMaxWegiht:
    def __init__(self, _fName, _maxIterations, _popSize, _initPop, _mutationRate,  _elite ):
        """
        Parameters and general variables
        Note not all parameters are currently used, it is up to you to implement how you wish to use them and where
        """

        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = int(_popSize)
        # self.crossoverProb   = float(_xoverProb)
        self.mutationRate   = float(_mutationRate)
        self.maxIterations  = int(_maxIterations)
        # self.trunkSize      = float(_trunk) 
        self.eliteSize      = float(_elite) 
        self.fName          = _fName
        self.initHeuristic  = int(_initPop)
        self.iteration      = 0
        self.data           = []
        self.elites = []
        self.target = 0

        self.readInstance()
        print("Initializing Population")
        self.initPopulation()


    def readInstance(self):
        """
        Reading an instance from fName
        """
        print("Reading File")
        file = open(self.fName, 'r')
        tVariables  = -1
        tClauses    = -1
        clause      = []
        variables   = []
        weights = []
        current_clause = []

        for line in file:
            data = line.split()

            if len(data) == 0:
                continue
            if data[0] == 'c':
                continue
            if data[0] == 'p':
                tVariables  = int(data[2])
                tClauses    = int(data[3])
                continue
            if data[0] == '%':
                break
            if tVariables == -1 or tClauses == -1:
                print ("Error, unexpected data")
                sys.exit(0)

            for i in range(0,len(data)):
                if i == 0:
                    weights.append(int(data[i]))
            ##now data represents a clause
            for var_i in data[1:]:
                literal = int(var_i)
                if literal == 0:
                    clause.append(current_clause)
                    current_clause = []
                    continue
                var = literal
                if var < 0:
                    var = -var
                if var not in variables:
                    variables.append(var)
                current_clause.append(literal)

        if tVariables != len(variables):
            print ("Unexpected number of variables in the problem")
            print ("Variables", tVariables, "len: ",len(variables))
            print (variables)
            sys.exit(0)
        if tClauses != len(clause):
            print(clause)
            print ("Unexpected number of clauses in the problem")
            sys.exit(0)
        file.close()
        self.target = sum(weights)
        self.data = [variables, clause,weights]
        print("File Reading Completed")

    def initPopulation(self):
        """
        Creating random individuals in the population
        """
        weights = []
        for i in range(0, self.popSize):
            print("Individual",i)
            individual = Individual(self.data,[],self.initHeuristic,i)
            individual.computeweight()
            print("Weight Computed")
            # print("I_weight",individual.getWeight())
            self.population.append(individual)
            weights.append(individual.getWeight())
        best_weight =  np.argmax(weights)
        self.best = self.population[best_weight]
        print ("Best initial sol: ",self.best.getWeight())
        
        if self.best.getWeight() == self.target:
            sol = []
            print("Target Was: ",self.target)
            print("Initial Solution is the best solution")
            print("Solution: ",self.best.truth_false_assignment)
            for i in self.best.truth_false_assignment:
                if i == -1:
                    sol.append(0)
                else:
                    sol.append(1)
            sys.exit(0)
        if self.eliteSize > 0:
            # Calling elitism to indentify best individuals in initial population
            self.elitism()

    def updateBest(self, candidate):
        if self.best.getWeight() < candidate.getWeight():
            self.best = candidate.copy()
            print ("iteration: ",self.iteration, "best: ",self.best.getWeight())

    def threeWayTournamentSelection(self):
        """
        Your Truncation Tournament Selection Implementation to fill the mating pool
        """
        tournament_pool = []
        weights = []
        for i in range(3):
            ind = self.population[random.randint(0,len(self.population)-1)]
            tournament_pool.append(ind)
            weights.append(ind.getWeight())
        winner = np.argmax(weights)
        return tournament_pool[winner]

    def crossover(self, indA, indB):
        """
        Executes a dummy crossover and returns the genes for a new individual
        """
        midP=int(len(indA.truth_false_assignment)/2)
        p1 =  indA.truth_false_assignment[0:midP]
        cgenes = p1 + indB.truth_false_assignment[midP:]
        # Here i am passuing the truth false value as genese, Inside the individual class the assigment of genes for child is done
        child = Individual(self.data, cgenes,self.initHeuristic)
        return child

    def bitFlipMutation(self, ind):
        """
        Mutate an individual by swapping  using bit flipping.
        """
        for i in range(len(ind.genes)):
            if random.random() < self.mutationRate:
                if i == 1:
                    ind.truth_false_assignment[i] = -1
                else:
                    ind.truth_false_assignment[i] = 1

    def newGeneration(self):
        """
        Creating a new generation
        1. Selection
        2. Crossover
        3. Mutation
        """
        for i in range(len(self.population)):
            """
            Depending of your experiment you need to use the most suitable algorithms for:
            1. Select two candidates
            2. Apply Crossover
            3. Apply Mutation
            """
            # Tournmanet Selection
            parent1 = self.threeWayTournamentSelection()  # Implemented 3 way tournament selection
            parent2 = self.threeWayTournamentSelection()  # Implemented 3 way tournament selection
            child = self.crossover(parent1,parent2) # as it is no changes
            self.bitFlipMutation(child)
            child.computeweight()
            self.updateBest(child)
            self.population[i]=child

            if self.eliteSize > 0:
                # Passing Elites no text generation
                self.population = self.population + self.elites
                # Calling elitism to indentify best individuals in new generation
                self.elitism()
              

    def elitism(self):
        elites = []
        population = []
        weights = []
        size = int(self.eliteSize*len(self.population))
        for i in self.population:
            weights.append(i.getWeight())
        elite_indexes = np.array(weights).argsort()[::-1][0:size]
        for i in range(len(self.population)):
            if i in elite_indexes:
                elites.append(self.population[i])
            else:
                population.append(self.population[i])
        self.population = population.copy()
        self.elites = elites.copy()


    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """
        print("GA Step Called")
        self.newGeneration()

    def search(self):
        """
        General search template.
        Iterates for a given number of steps
        """
        print("Search Called")
        self.iteration = 0
        sol = []
        while self.iteration < self.maxIterations:
            print("Iteration: ",self.iteration)
            random.seed(self.iteration+myStudentNum)
            self.GAStep()
            self.iteration += 1
            if self.best.getWeight() == self.target:
                print("Target Was: ",self.target)
                print ("Total iterations: ", self.iteration)
                print ("Best Solution: ", self.best.getWeight())
                for i in self.best.truth_false_assignment:
                    if i == -1:
                        sol.append(0)
                    else:
                        sol.append(1)
                print("Best Possible Solution Obtained:",self.best.truth_false_assignment)
                print("Best Solution Obtained:",sol)

                sys.exit(0)
        print("Target Was: ",self.target)
        print ("Total iterations: ", self.iteration)
        print ("Best Possible Solution Weight: ", self.best.getWeight())
        for i in self.best.truth_false_assignment:
            if i == -1:
                sol.append(0)
            else:
                sol.append(1)
        print("Best Possible Solution Obtained:",sol)

if len(sys.argv) < 6:
    print ("Error - Incorrect input")
    print ("Expecting python TSP.py [instance] [number of runs] [max iterations] [population size]", 
           "[initialisation method] [xover prob] [mutate prob] [truncation] [elitism] ")
    sys.exit(0)

inst, mItr ,pop, initH, pM, eliteP = sys.argv[1:]

# Calculating the Mutation Probability
pM = 1/int(pM)
'''
Reading in parameters, but it is up to you to implement what needs implementing
e.g. truncation selection, elitism, initialisation with heuristic vs random, etc'''
ga = GeniticMaxWegiht(inst, mItr,pop, initH, pM,  eliteP)
print("GA object created")
ga.search()


