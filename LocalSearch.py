''' 
Name : Peter Sunny Shanthveer Markappa
Subject: Meta-Heuristic Optimisation
Task: Local Search
'''


import re
import sys
import time
import random
import numpy as np
my_student_id = 208303 # Random number it can be your number but for different there will be different output

def readInstance(fName):
    file        = open(fName, 'r')
    tVariables  = -1
    tClauses    = -1
    clause      = []
    variables   = []

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

        ##now data represents a clause
        for var_i in data:
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
        print ("Unexpected number of clauses in the problem")
        sys.exit(0)
    file.close()
    return [variables, clause]



# -----------------------------------------------------------------
def solutionChecker(variables, clause):
    unsatClause = []
    for clause_ in clause:
        if len(set(clause_) & set(variables)) == 0:
            unsatClause.append(clause_)
    return unsatClause


# -----------------------------------------------------------------
# localSearch(variables, clauses, unsatClause, restarts, wp, p, tl, ipr)
def localSearch(variables, clauses, unsatClause, no_of_restarts, wp, p, tl, ipr):
    for try_ in range(no_of_restarts):
        print("Restart: ", try_)
        tabulist = []
        random.seed((try_+1)*my_student_id)
        no_unsat = len(unsatClause)
        print("Initial Unsatisfied Clauses: ", no_unsat)
        A = initialConfiguration(variables.copy())

        for flip_ in range(ipr):
            unsatClause = solutionChecker(A, clauses)
            if len(unsatClause) == 0:
                print("Solution Found")
                return A
            else:
                if len(unsatClause) < no_unsat:
                    print("Better Solution Found in Restart: ", try_)
                    print("Iteration: ", flip_)
                    print("Better Solution: ", no_unsat)
                    no_unsat = len(unsatClause)

                var = selectVariable_(A, unsatClause, wp,p,tabulist)
                A,tabulist = flip_X_from_A(A, var, p,tabulist,tl)
    return "No Solution Found"


def flip_X_from_A(A,X,p,tabulist,tl):
    '''flip the variable and add it into tabu list'''
    tabulist = checkTabu(tl,tabulist)
    tabulist.append(A[X])
    A[X] = -A[X]
    return A,tabulist


def checkTabu(tl,tabulist):
    '''
        Maintain TabuList Size
    '''
    if len(tabulist) >= tl:
        tabulist.pop()
        return tabulist
    return tabulist
    


# -----------------------------------------------------------------
# called from localSearch
def selectVariable_(A, unsatClause, wp,p,tabulist):
    # Choose an unsatisfied clause randomly
    randClause = random.choice(unsatClause)
    if random.random() < float(wp):
        # Choose a random variable from the clause
        randomValue_Literal = random.choice(randClause)
        if randomValue_Literal in A: # ignore sign
            return A.index(randomValue_Literal)
        else:
            randomValue_Literal *= -1
            return A.index(randomValue_Literal)
    else:
        netGainSol = []
        for i in range(len(randClause)):
            if randClause[i] in A:
                literalIndex=  A.index(randomValue_Literal)
            else:
                literalIndex = A.index(-randClause[i])

            A[literalIndex] *= -1
            solUnsatisfiesClause = solutionChecker(A, clauses)
            netgain = len(unsatClause) - len(solUnsatisfiesClause)
            netGainSol.append(netgain)
            A[literalIndex] *= -1
        Vbest = randClause[np.argmin(netGainSol)]
        if Vbest in A:
            VbestIndex = A.index(Vbest)
        else:
            VbestIndex = A.index(-Vbest)


        if A[VbestIndex] in tabulist or -A[VbestIndex] in tabulist:

            if random.random() < p:
                pop = netGainSol.pop(np.argmin(netGainSol))
                VsecondBest = randClause[np.argmin(netGainSol)]
                if VsecondBest in A:
                     VsecondBestIndex = A.index(VsecondBest)
                else:
                     VsecondBestIndex = A.index(-VsecondBest)
                VbestIndex = VsecondBestIndex
        return VbestIndex

# -----------------------------------------------------------------
def initialConfiguration(A):
    # randomly filipping the bit which are in A
    no_of_bitFlips = random.randrange(0, len(A))
    for i in range(no_of_bitFlips):
        random_index = random.randrange(0, len(A))
        A[random_index] *= -1
    return A


if __name__ == '__main__':

    # if len(sys.argv) < 6:
    #     print ("Error - Incorrect input")
    #     print ("----")
    #     sys.exit(0)

    arguments= sys.argv
    file_name = arguments[1] # instance name
    wp = float(arguments[2]) # walk probability
    p = float(arguments[3]) # some probability
    tl = int(arguments[4]) # Tabu list size
    ipr =int(arguments[5]) # Iterations per restart
    restarts = int(arguments[6]) # count of restart
    # fileName = sys.argv
    variables, clauses = readInstance(file_name)
    unsatClause = solutionChecker(variables, clauses)


    startTime = time.time()
    
    Solution = localSearch(variables, clauses, unsatClause, restarts, wp, p, tl, ipr)
    endTime = time.time()

    print(Solution)
    print("Total Time Taken : ", (endTime-startTime), "Seconds")


    




