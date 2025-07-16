import pandas as pd
import re

def extract_wavefunction_blocks(filename):
    """
    Extracts wavefunction blocks from an OUT36 output file.

    Parameters:
        filename (str): Path to the OUT36 file.

    Returns:
        List[str]: List of wavefunction block strings.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    blocks = []
    in_block = False
    current_block = []

    # Patterns to detect headers and block boundaries
    pnl_header_pattern = re.compile(r'pnl\(\s*\d?[spdfgh]\s*\)')
    r_nc_header_pattern = re.compile(r'\s*r\s*\(a0\)\s*nc', re.IGNORECASE)
    end_line_pattern = re.compile(r'^\s*\S+\s+\S+\s+nconf=', re.IGNORECASE)

    for i, line in enumerate(lines):
        # Start of new wavefunction block
        if pnl_header_pattern.search(line) and i + 1 < len(lines) and r_nc_header_pattern.search(lines[i + 1]):
            if in_block and current_block:
                blocks.append(''.join(current_block))
                current_block = []
            in_block = True
            current_block.append(line)
            current_block.append(lines[i + 1])
            continue

        if in_block:
            current_block.append(line)
            # End of current block
            if end_line_pattern.search(line) or (i + 1 < len(lines) and pnl_header_pattern.search(lines[i + 1])):
                blocks.append(''.join(current_block))
                current_block = []
                in_block = False

    if in_block and current_block:
        blocks.append(''.join(current_block))

    return blocks


def parse_pnl_data(raw_data: str) -> pd.DataFrame:
    """
    Parse raw orbital or score PNL data into a pandas DataFrame with inferred column names.

    Parameters:
        raw_data (str): The full text block containing headers and numerical data.

    Returns:
        pd.DataFrame: Parsed DataFrame with columns like ['r', 'nc', ... inferred columns ...].
    """
    lines = raw_data.strip().splitlines()

    # Step 1: Identify the label/header line
    label_line = next((line for line in lines if re.search(r'\w+\(\s*\d\w\)|\w+\(\w+\)', line)), None)
    if not label_line:
        raise ValueError("No recognizable column headers found (e.g., pnl(4p), rscore(i)).")

    # Step 2: Extract header names (supporting both pnl( 4p) and other function-style names)
    headers = re.findall(r'\w+\(\s*\d\w\)|\w+\(\w+\)', label_line)

    # Each label corresponds to two columns (e.g., values for mesh point 1 and 6)
    data_columns = [f"{h}_1" for h in headers] + [f"{h}_2" for h in headers]

    # Step 3: Filter numeric data lines
    data_lines = [line for line in lines if re.match(r'^\s*\d+\.\d+', line)]
    parsed_data = [list(map(float, line.split())) for line in data_lines]

    # Step 4: Construct DataFrame
    columns = ['r', 'nc'] + data_columns
    if parsed_data and len(columns) != len(parsed_data[0]):
        raise ValueError("Mismatch between number of columns and data width.")

    df = pd.DataFrame(parsed_data, columns=columns)
    return df


def combine_dataframes_by_index_columnwise(df_list, indexes):
    """
    Combines DataFrames between index points by column-wise merge (preserving row count).

    Parameters:
    - df_list: list of pandas DataFrames
    - indexes: list of int, positions to split and start new groups

    Returns:
    - list of combined DataFrames (with unique columns, same row count)
    """
    # Validate all items are DataFrames
    df_list = [df for df in df_list if isinstance(df, pd.DataFrame)]

    result = []
    start = 0
    for idx in indexes:
        group = df_list[start:idx]
        if group:
            combined = pd.concat(group, axis=1)
            result.append(combined)
        start = idx

    # Add remaining group
    if start < len(df_list):
        group = df_list[start:]
        combined = pd.concat(group, axis=1)
        result.append(combined)

    return result

def main(name):
    df_list_unparsed = extract_wavefunction_blocks(name)
    df_list_unparsed = df_list_unparsed[1:]
    indexes = []
    df_list_parsed = []

    for i, block in enumerate(df_list_unparsed):
        df = parse_pnl_data(block)
        df_list_parsed.append(df)

        if 'pnl( 1s)_1' in df.columns:
            indexes.append(i)



    dfs = combine_dataframes_by_index_columnwise(df_list_parsed, indexes)
    return(dfs) 

filename = f"InputOutputCowan\\ING11_0.txt"
dfs = main(filename)