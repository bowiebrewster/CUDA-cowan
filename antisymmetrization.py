import numpy as np
from itertools import combinations, product
from collections import Counter

def generate_microstates(l, w):
    """Generate all valid microstates for w equivalent electrons with orbital angular momentum l."""
    ml_values = list(range(-l, l + 1))
    ms_values = [-0.5, 0.5]
    
    # Generate all possible single-electron states
    single_electron_states = list(product(ml_values, ms_values))
    
    # Generate all valid combinations (Pauli exclusion)
    # Equivalent electrons can't occupy the same (ml, ms)
    microstates = list(combinations(single_electron_states, w))
    
    return microstates

def count_LS_terms(microstates, l, w):
    """Count unique (L, S) values from microstates."""
    LS_counter = Counter()
    for state in microstates:
        
        M_L = sum(ml for ml, ms in state)
        M_S = sum(ms for ml, ms in state)
        LS_counter[(abs(M_L), abs(M_S))] += 1
    # Now build term symbols and count how often each (L, S) occurs


    terms = Counter()
    for (M_L, M_S), count in LS_counter.items():
        if True: #here the symmetrization requirement
        #not (M_S == .5*w and M_L == l*w):
            terms[(abs(M_L), abs(M_S))] += 1

    return terms

def LS_term_symbol(MS, ML):
    L_letters = ['S', 'P', 'D', 'F', 'G', 'H', 'I', 'K']
    return f"{MS}{L_letters[ML]}"

def summarize_terms(l, w):
    microstates = generate_microstates(l, w)
    if False: 
        for value in microstates:
            print(value)
    term_counts = count_LS_terms(microstates, l ,w)
    if True: 
        for key,value in term_counts.items():
            print(key,value)


    print(f"LS terms for {w} equivalent electrons with l = {l}:")
    for (ML, MS), count in sorted(term_counts.items(), key=lambda x: (x[0][0], x[0][1])):
        term = LS_term_symbol(2*MS+1, ML)
        print(f"{term}: {count} configurations")

# Example usage:
summarize_terms(l=2, w=2)
#generate_microstates(l=1, w=2)# for 3 d-electrons (l=2)
