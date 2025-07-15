import re
from typing import Tuple, List

def parse_atomic_file(content: str) -> Tuple[str, List[str], List[str], List[str], List[str]]:
    """
    Parse a formatted atomic structure file into 5 logical sections.

    Returns:
        Tuple containing:
            - Section 1 (str): Header line (always the first line)
            - Section 2 (List[str]): Lines starting with a capital letter and a number (e.g. configuration info)
            - Section 3 (List[str]): Blocks starting with something like 'Sn5+ 4p64d...' with possible continuation lines
            - Section 4 (List[str]): Transition lines with dash (e.g. '4p54d10 - 4p64d84 ...')
            - Section 5 (List[str]): Remaining lines (interactions, tail data, etc.)
    """
    lines = content.strip().splitlines()

    section1 = lines[0]
    section2, section3, section4, section5 = [], [], [], []

    state = 2  # Track current section

    i = 1
    while i < len(lines):
        line = lines[i]

        if state == 2:
            if re.match(r'^[A-Z]\s+\d+', line):
                section2.append(line)
            else:
                state = 3
                continue

        elif state == 3:
            if re.match(r'^\w{1,2}\d*\+\s+\S+', line):
                block_lines = [line]
                i += 1
                while i < len(lines) and not re.match(r'^\s*\S+\s*-\s*\S+', lines[i]) and not re.match(r'^\w{1,2}\d*\+\s+\S+', lines[i]):
                    block_lines.append(lines[i])
                    i += 1
                section3.append("\n".join(block_lines))
                continue
            else:
                state = 4
                continue

        elif state == 4:
            if re.match(r'^\s*\S+\s*-\s*\S+', line):
                section4.append(line)
            else:
                state = 5
                continue

        elif state == 5:
            if line.strip():  # skip blank lines
                section5.append(line)

        i += 1

    return section1, section2, section3, section4, section5



string = f"""    1   -13 1 13 2 22         0111111 0 00000000 0 1000.0000 10.0     04-6 0 0             1  1  1  2  2
P 6  D 9  S 0  S 0  S 0  S 0  S 0  S 0  Sn5+   4p64d9      -1353475.442   0.0000
P 5  D10  F 0  S 0  S 0  S 0  S 0  S 0  Sn5+   4p54d10     -1352877.603   0.0000
P 6  D 8  F 1  S 0  S 0  S 0  S 0  S 0  Sn5+   4p64d84f1   -1352998.505   0.0000
Sn5+   4p64d9      2   5675090    336952        00        00        00hr99999999
Sn5+   4p54d10     2  65459050   3978752        00        00        00hr99999999
Sn5+   4p64d84f1  17  53368790   9984861   6640871 0.00E+001 0.00E+001hr99999999
 0.00E+001    350652      6352 0.00E+003   4944183 0.00E+003   2902693
   5363734 0.00E+004   3202634 0.00E+004   2221164
 4p54d10 - 4p64d84 2  80.17835  47.13865   0.00005   0.00005   0.00005hr99999999
Sn5+   4p64d9       Sn5+   4p54d10         1.29250( 4P//R1// 4D)-0.999hr -95 -99
Sn5+   4p64d9       Sn5+   4p64d84f1       1.67100( 4D//R1// 4F)-0.996hr -72 -98
                    -55555555.                                                  
                    -99999999.                                                  
   -1                                                                           
"""



for i, val in enumerate(parse_atomic_file(string)):
    if i > 0:
        for va in val:
            print(va, "\n")