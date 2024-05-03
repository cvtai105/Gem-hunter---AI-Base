def get_assignment_space(affirmative_literals, first, last):
    if first > last:
        return [affirmative_literals]
    
    assignment1 = affirmative_literals[:]
    assignment2 = affirmative_literals[:]
    assignment2[first] *= -1
    
    return get_assignment_space(assignment1, first + 1, last) + get_assignment_space(assignment2, first + 1, last)

print(get_assignment_space([1, 2, 3,6], 0, 3))