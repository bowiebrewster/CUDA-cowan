import pandas as pd
from itertools import product

def ConfigParse(configuration):
    if len(configuration) % 3 != 0:
        raise Exception("length of configuration must be mutiple of 3")
    
    configuration = configuration.lower()

    l_map = {'s': 0, 'p': 1, 'd': 2, 'f': 3, 'g': 4, 'h': 5, 'i': 6, 'k': 7, 'l':8, 'm':9, 'n':10 ,'o':11, 'q':12}

    parsed = []
    for i in range(int(len(configuration)/3)):

        ni = int(configuration[3 * i + 0])
        li = l_map[configuration[3 * i + 1]]
        wi = int(configuration[3 * i + 2])
        parsed.append((ni, li, wi))

    return parsed

#allowed symmetric electrons values ASEV
ASEV = pd.read_csv('permitted_ls_terms.csv')

#uncombined
def PossibleLSJ(configuration: str):
    result = {}

    # Step through the configuration in chunks of 3 characters
    for i in range(0, len(configuration), 3):
        conf_chunk = configuration[i:i+3]  # e.g., '4p3'
        n, l, w = ConfigParse(conf_chunk)[0]     # Assuming LandS returns a list with one tuple

        if w == 4 * l + 2:  # Full subshell, skip
            continue
        if w > 2 * l + 1:
            w = 4 * l + 2 - w # Holes are equivalent to electrons
            
        subset = ASEV[(ASEV['l'] == l) & (ASEV['w'] == w)]
        pairs = list(zip(subset['S'], subset['L']))

        if conf_chunk not in result:
            result[conf_chunk] = []

        result[conf_chunk].extend(pairs)

    return result


# we have sets of 

def min_signed_sum(values):
    min_val = float('inf')
    for signs in product([-1, 1], repeat=len(values)):
        total = sum(v * s for v, s in zip(values, signs))
        min_val = min(min_val, abs(total))
    return min_val

def generate_SL_pairs(Lmax, Lmin, Smax, Smin):

    SL_pairs = set()

    # Include half-integer and integer S values, step size 0.5
    s_values = [s * 0.5 for s in range(int(Smin * 2), int(Smax * 2) + 1)]
    
    # L is integer
    for L in range(Lmin, Lmax + 1):
        for S in s_values:
            SL_pairs.add((S, L))
    
    return SL_pairs

def total_possible_LS(config_dict):
    # Get all the lists of (S, L) tuples
    list_of_lists = list(config_dict.values())

    unionset = set()
    #print(list_of_lists)

    # combine 3p3 with 4d1 with 4f2 in that sense
    combinations = [list(p) for p in product(*list_of_lists)]

    #print(len(combinations))
    
    for entry in combinations:

        #print(entry)
        Slist, Llist  = zip(*entry)
        Slist, Llist = list(Slist), list(Llist)
        Slistmax = sum(Slist)
        Slistmin = min_signed_sum(Slist)
        Llistmax = int(sum(Llist))
        Llistmin = int(min_signed_sum(Llist))

        # each Lmax, Lmin, Smax, Smin produces a set of allowed pairs of S,L values which you can image as square in the S,L plane
        set0 = generate_SL_pairs(Llistmax, Llistmin, Slistmax, Slistmin)

        #print("\n",entry)
        #print(Slist, Llist)
        #print(Slistmin, Slistmax, Llistmin, Llistmax)
        #print(set0)

    unionset = unionset.union(set0)

    return unionset




