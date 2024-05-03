from itertools import combinations
from itertools import product
from pysat.solvers import Glucose3
import dpllhelper

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
    if(algorithm == "bruteforce"):
        solution = brute_force(cnf)
    elif (algorithm == "backtracking"):
        solution = backtracking(cnf)
    elif (algorithm == "pysat"):
        solution = pysatSolve(cnf)
    elif(algorithm == "dpll"):
        solution = DPLL(cnf)
    else:
        return None
  
    if solution == None:
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

def brute_force(cnf):
    def is_satisfying(model, cnf):
        for clause in cnf:
            satisfied = False
            for literal in clause:
                if literal in model:
                    satisfied = True
                    break
            if not satisfied:
                return False
        return True

    variables = {abs(literal) for clause in cnf for literal in clause}
    
    # Tạo tất cả các tổ hợp giá trị true/false cho các biến
    assignments = product([True, False], repeat=len(variables))
    
    # Kiểm tra từng tổ hợp
    for assignment in assignments:
        model = {var if value else -var for var, value in zip(variables, assignment)}
        if is_satisfying(model, cnf):
            return model
    
    # Nếu không có giải pháp nào, trả về None
    return None

def backtracking(cnf):
    def backtrack(model):
        if len(model) == len(variables):
            if is_satisfying(model):
                return model
            else:
                return None
        
        # Chọn một biến chưa được gán
        symbol = pick_unassigned_symbol(model)
        
        # Thử gán true và false cho biến và tiếp tục backtrack
        for value in [symbol, -symbol]:
            new_model = model.copy()
            new_model.add(value)
            result = backtrack(new_model)
            if result is not None:
                return result
        
        return None
    
    def is_satisfying(model):
        for clause in cnf:
            satisfied = False
            for literal in clause:
                if literal in model:
                    satisfied = True
                    break
            if not satisfied:
                return False
        return True
    
    def pick_unassigned_symbol(model):
        for v in variables:
            if v not in model and -v not in model:
                return v
        return None
    
    # Bắt đầu với một mô hình trống
    model = set()
    variables = {abs(literal) for clause in cnf for literal in clause}
    
    # Gọi hàm backtrack để tìm một mô hình thỏa mãn
    return backtrack(model)


def DPLL(formula):
    print("new call")
    assignment = []

    # // unit propagation:
    # while there is a unit clause {l} in Φ do
    #     Φ ← unit-propagate(l, Φ);
    while True:
        unit_clauses = [clause[0] for clause in formula if len(clause) == 1]
        if not unit_clauses:
            break
        for unit in unit_clauses:
            assignment.append(unit)
            formula = dpllhelper.unit_propagate(unit, formula)
        
    
    # // pure literal elimination:
    # while there is a literal l that occurs pure in formula do
    #     Φ ← pure-literal-assign(l, formuala);
    pure_literals = {literal for clause in formula for literal in clause}
    for literal in pure_literals:
        if -literal not in pure_literals:
            assignment.append(literal)
            formula = dpllhelper.pure_literal_assign(literal, formula)

    
    # // stopping conditions:
    # if Φ is empty then
    #     return true;
    # if Φ contains an empty clause then
    #     return false;
    if formula == []:
        return assignment
    if any(not clause for clause in formula):
        return []
    
    # // DPLL procedure:
    # l ← choose-literal(Φ);
    # return DPLL(Φ ∧ {l}) or DPLL(Φ ∧ {¬l});
    literal = dpllhelper.choose_literal(formula)
    
    formula1 = formula + [[literal]]
    formula2 = formula + [[-literal]]
    print(formula1)
    print(formula2)
    dpll1 = DPLL(formula1)
    print(formula2)

    dpll2 = DPLL(formula2)
    
    if dpll1 != []:
        return dpll1 + assignment
    elif dpll2 != []:
        return dpll2 + assignment
    
    return []


