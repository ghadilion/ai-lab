import sys
def get_input(filename):
    # Input follows the DIMACS format: https://www.cs.utexas.edu/users/moore/acl2/manuals/current/manual/index-seo.php/SATLINK____DIMACS
    f = open(filename, 'r')
    clauses = []
    for line in f:
        if line[0] in ['c','0','%']:
            continue
        elif line[0] == 'p':
            words = line.split()
            num_clauses = int(words[-1])
            num_variables = int(words[-2])
            symbols = list(range(1, num_variables+1))
        else:
            clause = [int(n) for n in line.split()]
            if(len(clause) != 4):
                continue
            if clause[-1] != 0:
                print('Error: Terminal number of one or more clauses is not 0!')
                return (None, None)
            clause = clause[:-1]
            if any(abs(n) > num_variables or abs(n) < 1 for n in clause):
                print('Error: Total number of variables exceeds limit!')
                return (None, None)
            clauses.append(clause)
    f.close()
    if len(clauses) != num_clauses:
        print('Error: Total number of clauses not equal to specification!')
        return (None, None)
    return (clauses, symbols)

def dpll_satisfiable(filename):
    clauses, symbols = get_input(filename)
    if clauses != None:
        return dpll(clauses, symbols, {})

def dpll(clauses, symbols, model):
    
    # if every clause in clauses is True in model then return True
    if check_all_clauses_true(clauses, model):
        print(f'\nModel = {model}\n')
        return True

    # if some clause in clauses is False in model then return False
    if check_some_clauses_false(clauses, model):
        return False
    
    # check for pure symbol
    P, value = find_pure_symbol(clauses, symbols, model)
    if P != None:
        new_symbols = symbols[:]
        new_symbols.remove(P)
        model[P] = value
        return dpll(clauses, new_symbols, model)
    
    # check for unit clause
    P, value = find_unit_clause(clauses, symbols, model)
    if P != None:
        new_symbols = symbols[:]
        new_symbols.remove(P)
        model[P] = value
        return dpll(clauses, new_symbols, model)
    
    # branch
    P, rest = symbols[0], symbols[1:]
    left_model, right_model = model.copy(), model.copy()
    left_model[P], right_model[P] = True, False
    return dpll(clauses, rest, left_model) or dpll(clauses, rest, right_model)


def check_all_clauses_true(clauses, model):
    for clause in clauses:
        if not any(abs(literal) in model.keys() and evaluate_literal(literal, model) == True for literal in clause):
            return False
    return True

def check_some_clauses_false(clauses, model):
    for clause in clauses:
        if all(abs(literal) in model.keys() and evaluate_literal(literal, model) == False for literal in clause):
            return True
    return False

def evaluate_literal(literal, model):
    if literal < 0:
        return not model[abs(literal)]
    else:
        return model[literal]

def find_pure_symbol(clauses, symbols, model):
    pure_symbols = symbols[:]
    visited_literals = []
    for clause in clauses:
        if any(abs(literal) in model.keys() and evaluate_literal(literal, model) == True for literal in clause):
            continue
        for literal in clause:
            if abs(literal) in pure_symbols:
                if -literal in visited_literals:
                    pure_symbols.remove(abs(literal))
                    visited_literals.remove(-literal)
                elif literal not in visited_literals:
                    visited_literals.append(literal)
    if len(pure_symbols) == 0:
        return (None, None)
    P = pure_symbols[0]
    value = P in visited_literals
    return (P, value)

def find_unit_clause(clauses, symbols, model):
    for clause in clauses:
        if any(abs(literal) in model.keys() and evaluate_literal(literal, model) == True for literal in clause):
            continue
        vars_in_clause = [literal for literal in clause if abs(literal) in symbols]
        if len(vars_in_clause) == 1:
            return (abs(vars_in_clause[0]), vars_in_clause[0] in symbols)
    return (None, None)

if len(sys.argv) != 2:
    print('Error: Incorrect number of command line arguments!')
else:
    filename = sys.argv[1]
    if dpll_satisfiable(filename):
        print('Satisfiable!\n')
    else:
        print('Not satisfiable!\n')
