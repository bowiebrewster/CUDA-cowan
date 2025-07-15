from itertools import combinations


def config_string_to_int(configuration : str):
    result = []

    # Step 1: Identify character positions
    char_positions = [i for i, c in enumerate(configuration) if c.isalpha()]

    for idx, pos in enumerate(char_positions):
        # Column 0: digit right before the character
        num_before = int(configuration[pos - 1]) if pos > 0 and configuration[pos - 1].isdigit() else None

        # Column 1: the character itself
        l_map = {'s': 0, 'p': 1, 'd': 2, 'f': 3, 'g': 4, 'h': 5, 'i': 6, 'k': 7}
        char = l_map[configuration[pos]]

        # Determine end of slice for column 2
        if idx + 1 < len(char_positions):
            next_pos = char_positions[idx + 1]
            slice_end = max(pos + 1, next_pos - 1)
        else:
            slice_end = len(configuration)  # last character: go to end

        # Column 2: digits from pos+1 up to slice_end
        digits_after = ''.join([c for c in configuration[pos + 1:slice_end] if c.isdigit()])
        third_col = int(digits_after) if digits_after else 1

        result.append([num_before, char, third_col])

    # Optional: propagate first digit in col 0 if consistent
    first_val = result[0][0]
    if all(row[0] == first_val for row in result if row[0] is not None):
        for row in result:
            row[0] = first_val

    return result

def doublecheck(lis:list):
    final_digits = {
        "Eav": 0,  # Always 1 Eav per configuration
        "Fk_ii": 0,  # Fk(li,li) for each subshell
        "zeta": 0,  # zeta_i for each subshell
        "Fk_ij": 0,  # Fk(li,lj) between subshells
        "Gk_ij": 0,  # Gk(li,lj) between subshells
        "Rk": 0
    }
    for entry in lis:
        final_digits[final_digits.keys()[entry[-1]]] += 1

    return final_digits



def main(configuration):
    configarray = config_string_to_int(configuration)
    #print(configarray)

    # Initialize counts
    counts = {
        "Eav": 1,  # Always 1 Eav per configuration
        "Fk_ii": 0,  # Fk(li,li) for each subshell
        "zeta": 0,  # zeta_i for each subshell
        "Fk_ij": 0,  # Fk(li,lj) between subshells
        "Gk_ij": 0,  # Gk(li,lj) between subshells
    }
    """
    from documentation
    in this list, "Fk" represents F2, F4, ... Fm [m=min(2li,2lj)], and 
    "Gk" represents G|li-lj|, ... Gli+lj, with index k incremented by 2.  
    There are no Fk(li,li) unless 2.LE.wi.LE.4li;
    there are no Fk(li,lj) nor Gk(li,lj), i < j, unless 1.LE.w.LE.4l+1 for both wi and wj; 
    and there are no Fk of either type unless both l are greater than zero.
    There is no zetai unless 1.LE.wi.LE.4li+1 and li > 0.  
    If IABG > 0, any parameters a,b,g,T,T1,T2 for subshell i follow the corresponding
    Fk(li,li).  If IABG = 2 or 4, then "Fk" represents F1, F2, F3, ... Fm, 
    and k likewise increases in unit steps for the Gk.
    """
    #print("configarray: ",configarray)

    for row in configarray:
        [ni, li, wi] = row

        if 2 <= wi <= 4 * li:  # There are no Fk(li,li) unless 2.LE.wi.LE.4li;
            counts['Fk_ii'] += li

        if 1 <= wi <= 4 * li + 1 and li > 0: #There is no zetai unless 1.LE.wi.LE.4li+1 and li > 0. 
            counts['zeta'] += 1 

    if len(configarray) > 1:
        for row1, row2 in combinations(configarray, 2):
            #print(row1, row2)
            [ni, li, wi] = row1
            [nj, lj, wj] = row2
            
            if 1 <= wi <= 4 * li + 1 and 1 <= wj <= 4 * lj + 1:  # there are no Fk(li,lj) nor Gk(li,lj), i < j, unless 1.LE.w.LE.4l+1 for both wi and wj
                counts['Fk_ij'] += min(li,lj)
                counts['Gk_ij'] += int(((li + lj) - abs(li-lj))/2 + 1)

   
    return counts

