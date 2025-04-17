
def count_parameters(configuration):
    """
    Counts the number of Eav, Fk, zeta, and other parameters for a given electron configuration.

    Args:
        configuration (str): The electron configuration (e.g., "4p54d2").

    Returns:
        dict: A dictionary with counts of Eav, Fk, zeta, Fk_ij, and Gk_ij parameters.
    """

    if len(configuration) != 6:
        raise Exception("Configuration must be length 6 others not implemented")
    

    l_map = {'s': 0, 'p': 1, 'd': 2, 'f': 3, 'g': 4, 'h': 5, 'i': 6, 'k': 7}

    ni = int(configuration[0])
    li = l_map[configuration[1]]
    wi = int(configuration[2])
    nj = int(configuration[3])
    lj = l_map[configuration[4]]
    wj = int(configuration[5])


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



    if 2 <= wi <= 4 * li:  # There are no Fk(li,li) unless 2.LE.wi.LE.4li;
        counts['Fk_ii'] += li 
    if 2 <= wj <= 4 * lj:  # There are no Fk(li,li) unless 2.LE.wi.LE.4li;
        counts['Fk_ii'] += lj

    if 1 <= wi <= 4 * li + 1 and 1 <= wj <= 4 * lj + 1:  # there are no Fk(li,lj) nor Gk(li,lj), i < j, unless 1.LE.w.LE.4l+1 for both wi and wj
        counts['Fk_ij'] += min(li,lj)
        counts['Gk_ij'] += int(((li + lj) - abs(li-lj))/2 + 1)

    if 1 <= wi <= 4 * li + 1 and li > 0: #There is no zetai unless 1.LE.wi.LE.4li+1 and li > 0. 
        counts['zeta'] += 1
    if 1 <= wj <= 4 * lj + 1 and lj > 0: #There is no zetai unless 1.LE.wi.LE.4li+1 and li > 0. 
        counts['zeta'] += 1    

    return counts

