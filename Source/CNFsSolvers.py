from itertools import combinations
from itertools import product
from pysat.solvers import Glucose3
import dpll
import bruteforce
import backtracking

def GenerateCNFsFromMatrix(matrix):
    """
    If input.txt contains:
    3, _, 2, _
    _, _, 2, _
    _, 3, 1, _
    then
    the matrix param should be:
    x, x, x, x, x, x
    x, 3, None, 2, NONE, x
    x, None, None, 2, NONE, x
    x, NONE, 3, 1, NONE, x
    x, x, x, x, x, x
    """
    clauses = []
    n = len(matrix[0])
    m = len(matrix)
    for i in range(1, m-1):
        for j in range(1, n-1):
            if matrix[i][j] != '_':
                trueArr = []
                falseArr = []
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if matrix[x][y] == '_':
                            falseArr.append(-(x*n + y))
                            trueArr.append(x*n + y)
                for combination in combinations(falseArr, matrix[i][j] + 1):
                    clauses.append(combination)
                for combination in combinations(trueArr, len(trueArr) - matrix[i][j] + 1):
                    clauses.append(combination)

    clauses = list(set(clauses))
    
    #convert to list of lists
    clauses = [list(clause) for clause in clauses]

    return clauses

def GetRevealedMatrix(matrix, cnf, algorithm = "pysat"):
    print('Matrix size:', len(matrix) -2, 'x', len(matrix[0]) -2)
    print('CNF count:', len(cnf))
    print('Variable count:', len({abs(literal) for clause in cnf for literal in clause}))
    print('Solving with:', algorithm)
    if(algorithm == "bruteforce"):
        solution = bruteforce.solve(cnf)
    elif (algorithm == "backtracking"):
        solution = backtracking.solve(cnf)
    elif (algorithm == "pysat"):
        solution = pysatSolve(cnf)
    elif(algorithm == "dpll"):
        solution = dpll.solve(cnf)
    else:
        return None
    print('Done')
    print()
  
    if solution == None:
        print('none')
        return matrix
    
    
    
    n = len(matrix[0])
    m = len(matrix)

    # for i in range(len(solution), m*(n-1)):
    #     solution.append(-i)
    for i in solution:
        j = abs(i)
        x = j // n
        y = j % n
        if i > 0:
            matrix[x][y] = 'T'
        else:
            if matrix[x][y] == '_':
                matrix[x][y] = 'G'
    
    return matrix
        

def pysatSolve(cnf):
    solver = Glucose3()
    for clause in cnf:
        solver.add_clause(clause)
    if solver.solve():
        return solver.get_model()
    else:
        return None

