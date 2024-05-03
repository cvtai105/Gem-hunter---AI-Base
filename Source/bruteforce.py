
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

def solve(cnf):
    affirmative_literals = {abs(literal) for clause in cnf for literal in clause}
    assignment_space = get_assignment_space(list(affirmative_literals), 0, len(affirmative_literals) - 1)
    for assignment in assignment_space:
        if evaluate_cnf(cnf, assignment):
            return assignment
    return None


    
def get_assignment_space(affirmative_literals, first, last):
    if first > last:
        return [affirmative_literals]
    
    assignment1 = affirmative_literals[:]
    assignment2 = affirmative_literals[:]
    assignment2[first] *= -1
    
    return get_assignment_space(assignment1, first + 1, last) + get_assignment_space(assignment2, first + 1, last)