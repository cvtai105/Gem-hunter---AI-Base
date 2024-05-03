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