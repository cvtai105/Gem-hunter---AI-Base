import os
import dpll
import backtracking
import bruteforce
import time
import CNFsSolvers

def getDpllRuntime(cnf):
    print('Running dpll ...')
    start = time.time_ns()
    dpll.solve(cnf)
    end = time.time_ns()
    print('Done')
    return (end - start)

def getBacktrackingRuntime(cnf):
    print('Running back tracking ...')
    start = time.time_ns()
    print
    backtracking.solve(cnf)
    end = time.time_ns()
    print('Done')
    return (end - start)

def getBruteforceRuntime(cnf):
    print('Running bruteforce ...')
    start = time.time_ns()
    bruteforce.solve(cnf)
    end = time.time_ns()   
    print('Done')
    return (end - start)

def getPysatRuntimme(cnf):
    print('Running pysat ...')
    start = time.time_ns()
    CNFsSolvers.pysatSolve(cnf)
    end = time.time_ns()   
    print('Done')
    return (end - start)