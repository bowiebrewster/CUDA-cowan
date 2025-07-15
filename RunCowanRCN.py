import subprocess
import os
import re


def run_shell_script():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    port_script = os.path.join(script_dir, "port.sh")
    bash_path = "C:\\Program Files\\Git\\bin\\bash.exe"

    try:
        # Run the shell script using the full path to bash.exe
        print("Running port.sh...")
        result = subprocess.run([bash_path, port_script], check=True, text=True, capture_output=True)
        print(result.stdout)  # Print the output of the shell script
        print("port.sh completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Shell script output: {e.stdout}")
        print(f"Shell script error: {e.stderr}")
        exit(1)

#rename outputfiles to txtfiles for easier reading
def totxt(index:int, substr: str):
    # Get the directory where the Python script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    path = f"{script_dir}/InputOutputCowan/{substr}"
    topath = f"{script_dir}/InputOutputCowan/{substr}_{index}.txt"

    if os.path.exists(path):
        # Delete the .txt version if it already exists
        if os.path.exists(topath):
            os.remove(topath)
            print(f"Deleted existing file {substr}.txt.")

        # Rename the file
        os.rename(path, topath)
        #print(f"Renamed {substr} to {substr}.txt.")
    else:
        print(f"File {substr} not found.")

def format_line(prefix, suffix):
    spaces_needed = 34 - len(prefix)
    spaces = ' ' * max(spaces_needed, 1)  # at least 1 space
    return f"{prefix}{spaces}{suffix}"


def write36(lines:list, m:int):
    allres = ["200-90 0 2  01.  0.2    5.E-08    1.E-11-2 00190 0 1.0  0.65  0.0 1.00   -6"]

    for line in lines:
        [part1,part2,part3,part4] = line(m)
        #print(par1,par2,part3,part4)

        match = re.match(r'(\d+)[A-Za-z]+(\d+)', part2)
        first_numbers = match.group(1)
        second_numbers = match.group(2)

        spacing1 = " " * (5 - (len(first_numbers)))
        spacing2 = " " * (4 - (len(second_numbers)))
        spacing3 = " " * (34 - len(part1) - len(part2) - len(part3) - len(spacing1) - len(spacing2))

        res = part1 + spacing1 + part2 + spacing2 + part3 + spacing3 + part4
        allres.append(res)

    allres.append("   -1")
    mainstr = "\n".join(allres)

    return mainstr
