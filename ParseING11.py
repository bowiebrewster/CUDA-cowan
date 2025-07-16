import re
from typing import Tuple, List, Dict

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


def parse_section2(lines: List[str]) -> Dict[Tuple[str, str], float]:
    result = {}

    for line in lines:
        tokens = line.split()

        # Collect config parts that are NOT "S 0", "F 0", etc.
        config_parts = []
        i = 0
        while i < len(tokens):
            token = tokens[i]

            # If it's a capital config like P, D, F, S and followed by a 0, skip both
            if token in {"S", "F"} and i + 1 < len(tokens) and tokens[i + 1] == "0":
                i += 2
                continue

            # If token is something like 'Sn5+', that's our element name
            if re.match(r'^\w{1,2}\d*\+$', token):
                element = token
                break  # Stop scanning config tokens
            else:
                config_parts.append(token)
                i += 1

        # Get the energy value (assumed to be second-last float on the line)
        try:
            energy = float(tokens[-2])
        except (ValueError, IndexError):
            continue  # Skip malformed lines

        key = (element, " ".join(config_parts))
        result[key] = energy

    return result


def parse_section3(blocks: List[str]) -> Dict[Tuple[str, str], List[int]]:
    """
    Parse Section 3 blocks using the first number as a count of how many meaningful integers follow.

    Args:
        blocks (List[str]): List of strings (each block can be multiline)

    Returns:
        Dict[Tuple[str, str], List[int]]: Keys are (element, config), values are full numeric data lists
    """
    result = {}

    for block in blocks:
        # Flatten multiline blocks into a single line
        flat = " ".join(block.splitlines())
        tokens = flat.split()

        # Extract element and configuration
        try:
            element = tokens[0]
            config = tokens[1]
        except IndexError:
            continue

        # Collect integers, ignoring invalid or placeholder tokens
        numbers = []
        for token in tokens[2:]:
            if token == '00' or re.match(r'^0\.00E\+\d+$', token) or token.startswith('hr'):
                continue
            try:
                val = int(token)
                numbers.append(val)
            except ValueError:
                continue

        if numbers:
            count = numbers[0]
            expected = numbers[:count + 1]  # Include count itself + the specified number of entries
            result[(element, config)] = expected

    return result

def parse_section4(lines: List[str]) -> Dict[Tuple[str, str], List[float]]:
    """
    Parse Section 4 lines to extract orbital transitions and associated float values.

    Args:
        lines (List[str]): Lines from Section 4

    Returns:
        Dict[Tuple[str, str], List[float]]: Keys are (orbital1, orbital2),
                                            values are a list of three floats
    """
    result = {}

    for line in lines:
        tokens = line.split()
        try:
            # Locate the dash separator
            dash_index = tokens.index('-')
            orb1 = tokens[dash_index - 1]
            orb2 = tokens[dash_index + 1]
        except (ValueError, IndexError):
            continue  # Skip malformed lines

        # Extract up to 3 floats after the dash
        floats = []
        for token in tokens[dash_index + 2:]:
            if token.startswith('hr'):
                break
            try:
                floats.append(float(token))
            except ValueError:
                continue

        if len(floats) >= 3:
            result[(orb1, orb2)] = floats[:3]

    return result

#TODO interpret section 1 and section 5 if necesarry

def main(path):
    with open(path, 'r') as f:
        content = f.read()

    section1, section2, section3, section4, section5 = parse_atomic_file(content)

    dict2 = parse_section2(section2)
    dict3 = parse_section3(section3)
    dict4 = parse_section4(section4)
    

    return dict2, dict3, dict4
