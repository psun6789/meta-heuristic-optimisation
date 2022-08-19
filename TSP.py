"""
Author: Peter Sunny Shanthveer Markappa

"""
import time
import random, sys
from Individual import *

myStudentNum = 208303 # Replace 12345 with your student number
random.seed(myStudentNum)

class BasicTSP:
    def __init__(self, _fName, nRuns, _maxIterations, _popSize, _initPop, _xoverProb, _mutationRate, _trunk,  _elite):
        """
        Parameters and general variables
        Note not all parameters are currently used, it is up to you to implement how you wish to use them and where
        """
        '''Here I have taken nRuns'''
        self.nRuns = int(nRuns)
        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = int(_popSize)
        self.genSize        = None
        self.crossoverProb   = float(_xoverProb)
        self.mutationRate   = float(_mutationRate)
        self.maxIterations  = int(_maxIterations)
        self.trunkSize      = float(_trunk)
        self.eliteSize      = float(_elite)
        self.fName          = _fName
        self.initHeuristic  = int(_initPop)
        self.iteration      = 0
        self.data           = {}
        """This are the created by me"""
        '''cerating empty list for storing top population'''
        self.top_population = []
        '''creating this to count the truncation'''
        self.pop_elitism = []
        self.truncation_count = None
        self.new_population = []
        self.new_population_count = None

        '''Calling readInstance and initPopulation method'''
        self.readInstance()
        self.initPopulation()
        print(self.popSize,self.crossoverProb,self.mutationRate,self.maxIterations,self.trunkSize,self.eliteSize)


    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (cid, x, y) = line.split()
            self.data[int(cid)] = (int(x), int(y))
        file.close()

    def initPopulation(self):
        """
        Creating random individuals in the population
        """
        for i in range(0, self.popSize):
            individual = Individual(self.genSize, self.data, [], self.initHeuristic)
            '''Checking whether it is random based (0) or Nearest neighbout(1)
            '''
            if self.initHeuristic == 0 or self.initHeuristic == 1:
                individual.computeFitness()
                self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
                self.top_population.append(self.best.genes)

        self.top_population.reverse()
        self.truncation_count = int(self.trunkSize * self.popSize)
        print ("Best initial sol: ", self.best.getFitness())

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
            ga.elitism()
            print ("iteration: ",self.iteration, "best: ",self.best.getFitness())



    # def randomSelection(self):
    #     """
    #     Random (uniform) selection of two individuals
    #     """
    #     indA = self.matingPool[ random.randint(0, self.popSize-1) ]
    #     indB = self.matingPool[ random.randint(0, self.popSize-1) ]
    #     return [indA, indB]

    def truncationSelection(self):
        if len(self.top_population) < self.truncation_count :
            indA = self.top_population[random.randint(0, len(self.top_population) - 1)]
            indB = self.top_population[random.randint(0, len(self.top_population) - 1)]
        else:
            indA = self.top_population[random.randint(0, self.truncation_count - 1)]
            indB = self.top_population[random.randint(0, self.truncation_count - 1)]
        return [indA, indB]

    def order1Crossover(self, indA, indB):
        """
            for this I have below website
            https://stackoverflow.com/questions/50489450/genetic-algorithm-ordered-crossover-in-python
        """
        population_list = ['population_1', 'population_2']
        global child, cgenes, new_child
        tgenes = []
        if random.random() > self.crossoverProb:
           parent = random.choice(population_list)
           if parent == population_list[0]:
               child = Individual(self.genSize, self.data, indA, self.initHeuristic)
           elif parent == population_list[1]:
               child = Individual(self.genSize, self.data, indB, self.initHeuristic)
           return child
        else:
           """cutting the genesize at 2 points for crossover"""
           """ joining the first part of the of chromosomes, middle part and joining the third part """
           # new_gen = indA[random.randint(0, (int(0.5 * self.genSize)) - 1):random.randint((int(0.5 * self.genSize))+1 , self.genSize - 1)]
           # new_gen = indA[random.randint(0, (int(0.75 * self.genSize)) - 1):random.randint((int(0.75 * self.genSize))+1 , self.genSize - 1)]
           new_gen = indA[random.randint(0, (int(0.25 * self.genSize)) - 1):random.randint((int(0.25 * self.genSize))+1 , self.genSize - 1)]
           for new in range(len(indB)):
             if indB[new] in new_gen: continue
             else: tgenes.append(indB[new])

           for new_g in range(len(new_gen)):
                tgenes.append(new_gen[new_g])
                cgenes = tgenes
           child = Individual(self.genSize, self.data, cgenes, self.initHeuristic)
           return child

    def inversionMutation(self, ind):
        geneSequence = ind.genes
        i = 0
        """
        For this i have refered this site
            https://codereview.stackexchange.com/questions/115230/travelling-salesman-problem-using-ga-mutation-and-crossover
        """
        if random.random() > self.mutationRate:
           return
        else:
            # """ This method is working but the performance is very less so i have applied another method """
            # sequenceA = random.randint(0, len(geneSequence)-1)
            # sequenceB = random.randint(sequenceA, len(geneSequence)-1)
            # reverseSequence = geneSequence[sequenceA:sequenceB]
            # reverseSequence.reverse()
            #
            # while index in range(sequenceA, sequenceB):
            #     geneSequence[index] = reverseSequence[i]
            #     i+=1
            #     index+=1
            # ind.setGenes(geneSequence)
            # ind.computeFitness()
            # self.updateBest(ind)

            """You can implement different combition of inverion of mutation"""
            sequenceA = random.randint(0, (int(0.5 * self.genSize)) - 1)
            sequenceB = random.randint((int(0.5 * self.genSize)) + 1, self.genSize - 1)
            inverse_part = ind.genes[sequenceA:sequenceB]
            """middle part reversing for inverse mutation"""
            inverse_part.reverse()
            ind.genes = ind.genes[0:sequenceA] + inverse_part + ind.genes[sequenceB:]

    def crossover(self, indA, indB):
        """
        Executes a dummy crossover and returns the genes for a new individual
        """
        population_1 =  indA[0:int(0.25 * self.genSize)]
        cgenes = int(0.25 * self.genSize) + [i for i in indB if i not in int(0.75 * self.genSize)]
        child = Individual(self.genSize, self.data, cgenes, self.initHeuristic)
        return child

    def mutation(self, ind):
        """
        Mutate an individual by swapping two cities with certain probability (i.e., mutation rate)
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation
        Note this is not survival of the fittest as just putting one copy of every chromosome in prev pop
        """
        self.matingPool = []
        for ind_i in self.population:
            self.matingPool.append( ind_i.genes )

        # if self.iteration !=0 and self.eliteSize !=0 and len(self.newpop)!=0:
        #     self.newpop.reverse()
        #     self.newpopcht = int(self.eliteSize) * len(self.toppop)

    def elitism(self):
        if self.eliteSize !=0:
            self.new_population.append(self.best.genes)
        else:
            self.pop_elitism.append((self.best.genes))

    def newGeneration(self):
        """
        Creating a new generation
        1. Selection
        2. Crossover
        3. Mutation
        """
        for i in range(self.popSize):
            """
            Depending of your experiment you need to use the most suitable algorithms for:
            1. Select two candidates
            2. Apply Crossover
            3. Apply Mutation
            """
            parent1, parent2 = self.truncationSelection()
            child = self.order1Crossover(parent1, parent2)
            self.inversionMutation(child)
            child.computeFitness()
            self.updateBest(child)
            self.population[i]=child

    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """

        self.updateMatingPool()
        self.newGeneration()

    def search(self):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep()
            self.iteration += 1

        print ("Total iterations: ", self.iteration)
        print ("Best Solution: ", self.best.getFitness())



if __name__ == '__main__':

    if len(sys.argv) < 9:
        print ("Error - Incorrect input")
        print ("Expecting python TSP.py [instance] [number of runs] [max iterations] [population size]",
               "[initialisation method] [xover prob] [mutate prob] [truncation] [elitism] ")
        sys.exit(0)

    f, inst, nRuns, nIters, pop, initH, pC, pM, trunkP, eliteP = sys.argv
    '''
    Reading in parameters, but it is up to you to implement what needs implementing
    e.g. truncation selection, elitism, initialisation with heuristic vs random, etc'''
    if int(initH) > 1:
        print("Choose either 0 or 1 for initialization method")
    else:
        print("File Name : ", f)
        print("Total Runs you choosen : ", nRuns)
        print("Iteration for Each Run : ", nIters)
        print("Population size : ", pop)
        print("Elitism : ", eliteP)
        if float(eliteP)>1.0:
            print("--------Elitism must be between 0.0 to 1.0-----")
        else:
            ga = BasicTSP(inst, nRuns, nIters, pop, initH, pC, pM, trunkP, eliteP)
            star_time = time.time()
            for ind in range(0, ga.nRuns):
                i_star_time = time.time()
                print("Runs : ", ind)
                ga.search()
                # ga.updateBest()
                i_end_time = time.time()
                print()
                print("------------------Run", ind, "Iteration Time :", i_end_time - i_star_time,"-----------------------------------")
            end_time = time.time()
            print("Total Time :", end_time - star_time)