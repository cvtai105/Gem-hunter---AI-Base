def unit_propagate(l, formula):
    for clause in formula[:]:
        if l in clause:
            formula.remove(clause)
        elif -l in clause:
            clause.remove(-l)

    return formula

def pure_literal_assign(l, formula):
    for clause in formula[:]:
        if l in clause:
            formula.remove(clause)
    return formula

def choose_literal(formula):
    return formula[0][0]

def solve(formula):
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
            formula = unit_propagate(unit, formula)

    # // pure literal elimination:
    # while there is a literal l that occurs pure in formula do
    #     Φ ← pure-literal-assign(l, formuala);
    pure_literals = {literal for clause in formula for literal in clause}
    for literal in pure_literals:
        if -literal not in pure_literals:
            assignment.append(literal)
            formula = pure_literal_assign(literal, formula)

    # // stopping conditions:
    # if Φ is empty then
    #     return true;
    # if Φ contains an empty clause then
    #     return false;
    if formula == []:
        return assignment
    if any(not clause for clause in formula):
        return None
    
    # // DPLL procedure:
    # l ← choose-literal(Φ);
    # return DPLL(Φ ∧ {l}) or DPLL(Φ ∧ {¬l});
    literal = choose_literal(formula)

    
    dpll1 = solve([row[:] for row in formula] + [[literal]])
    if dpll1 != None:
        return dpll1 + assignment

    dpll2 = solve([row[:] for row in formula] + [[-literal]])
    if dpll2 != None:
        return dpll2 + assignment
    
    return None


