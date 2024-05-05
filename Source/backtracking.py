def evaluate_clause(clause, assignment):
    for l in clause:
        if l in assignment:
            return True
    return False

def evaluate_cnf(cnf, assignment):
    for clause in cnf:
        if not evaluate_clause(clause, assignment):
            return False
    return True



def bakctrack(cnf, assignment, first, last):
    if first > last:
        if evaluate_cnf(cnf, assignment):
            return assignment
        return None

    assignment2 = assignment[:]
    assignment2[first] *= -1

    return bakctrack(cnf, assignment, first + 1, last) or bakctrack(cnf, assignment2, first + 1, last)


def solve(cnf):
    assigment = {abs(literal) for clause in cnf for literal in clause}
    return bakctrack(cnf, list(assigment), 0, len(assigment) - 1)