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


blocks = extract_wavefunction_blocks(f"InputOutputCowan\\OUT36_0.txt")
for i, block in enumerate(blocks):
    print(f"--- Block {i+1} ---")
    print(block)  # Preview first 500 characters
