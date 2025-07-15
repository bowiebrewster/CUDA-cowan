from sympy import S, symbols, binomial, factorial, Rational, Sum, expand, simplify
from sympy.physics.wigner import wigner_3j, wigner_6j

# Placeholder for Rk function – define this appropriately
def Rk(k, l1, l2, l3, l4):
    # Provide actual definition here
    return 1

def A(l1, l2, l3, l4):
    pre_factor = (2*l1 + 1)*(2*l2 + 1)*(2*l3 + 1)*(2*l4 + 1)
    tj1 = wigner_3j(l1, 1, l4, 0, 0, 0)
    tj2 = wigner_3j(l2, 1, l3, 0, 0, 0)
    
    term1 = pre_factor * tj1 * tj2 * (8/3) * tj1 * tj2 * Rk(None, l1, l2, l4, l3)
    
    sum_expr = 0
    for k in range(abs(l1 - l3), l1 + l3 + 1, 2):
        sj = wigner_6j(l1, l3, k, l2, l4, 1)
        tj3 = wigner_3j(l1, k, l3, 0, 0, 0)
        tj4 = wigner_3j(l2, k, l4, 0, 0, 0)
        sum_expr += sj * tj3 * tj4 * Rk(k, l1, l2, l3, l4)
    
    term2 = (4 * (-1)**(l1 + l3) * sum_expr * pre_factor * tj1 * tj2)
    
    return simplify(term1 + term2)

def DClass(N1, N2, N3, N4, l1, l2, l3, l4, caseNumber):
    if caseNumber == 1:
        expr = binomial(4*l1 + 1, N1 - 1) * binomial(4*l2 + 1, N2) * binomial(4*l3 + 1, N3 - 1) * binomial(4*l4 + 1, N4)
    elif caseNumber == 2:
        expr = binomial(4*l1, N1 - 1) * binomial(4*l3 + 1, N3 - 1) * binomial(4*l4 + 1, N4)
    elif caseNumber == 3:
        expr = binomial(4*l1 + 1, N1 - 1) * binomial(4*l2, N2) * binomial(4*l3 + 1, N3 - 1)
    elif caseNumber == 4:
        expr = binomial(4*l1, N1 - 2) * binomial(4*l2 + 1, N2) * binomial(4*l4 + 1, N4)
    elif caseNumber == 5:
        expr = binomial(4*l1, N1 - 1) * binomial(4*l3, N3 - 1)
    else:
        return "Invalid case number. Use 1–5."
    
    return expr

def Q(N1, N2, N3, N4, l1, l2, l3, l4, caseNumber):
    return A(l1, l2, l3, l4) * DClass(N1, N2, N3, N4, l1, l2, l3, l4, caseNumber)
