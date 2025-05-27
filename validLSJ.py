from itertools import combinations, product

def get_ml_values(l):
    return list(range(-l, l + 1))

def get_ms_values():
    return [-0.5, 0.5]

def generate_configurations(l, e):
    ml_vals = get_ml_values(l)
    ms_vals = get_ms_values()
    orbitals = list(product(ml_vals, ms_vals))
    return list(combinations(orbitals, e))

def total_L_and_S(config):
    L = sum(ml for ml, ms in config)
    S = sum(ms for ml, ms in config)
    return L, S

def possible_J(L, S):
    min_J = abs(L - S)
    max_J = L + S
    return [j for j in range(int(2 * min_J), int(2 * max_J) + 1, 1)]  # 2*J
    # Dividing by 2 later to get float J

def calculate_LSJ(n1, l1, e1, n2, l2, e2):
    configs1 = generate_configurations(l1, e1)
    configs2 = generate_configurations(l2, e2)

    LS_set = set()
    for c1 in configs1:
        for c2 in configs2:
            full_config = c1 + c2
            if len(set(full_config)) == len(full_config):  # Pauli exclusion
                L, S = total_L_and_S(full_config)
                LS_set.add((L, S))

    results = set()
    for L, S in LS_set:
        for j2 in possible_J(L, S):
            results.add((L, S, j2 / 2))  # convert 2*J back to J

    return sorted(results, key=lambda x: (x[0], x[1], x[2]))

# Example input: 4p6 4d1 => [4,1,6,4,2,1]
if __name__ == "__main__":

    LSJ = calculate_LSJ(4 ,3 ,6 ,4 ,2 ,1)
    print("Possible (L, S, J) values:")
    for L, S, J in LSJ:
        print(f"L = {L}, S = {S}, J = {J}")
