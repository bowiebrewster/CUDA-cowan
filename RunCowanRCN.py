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


def line1(m):
    return [f"   50",f"{m+6}Sn{m+5}+", f"4p64d{9-m}", f"3d10 4s2 4p6 4d{9-m}"]
def line2(m):
    return [f"   50",f"{m+6}Sn{m+5}+", f"4p54d{10-m}", f"3d10 4s2 4p6 4d{10-m}"]
def line3(m):
    return [f"   50",f"{m+6}Sn{m+5}+", f"4p64d{8-m}4f1", f"3d10 4s2 4p6 4d{8-m} 4f1"]

lines = [line1, line2, line3]

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

def main():
    for m in range(0, 1):
        # write the in 36 file
        mainstr = write36(lines, m)
        filename = f"C:\\Users\\brewster\\Desktop\\CowanFrontend\\InputOutputCowan\\IN36"
        with open(filename, "w") as f:
            f.write(mainstr)

        # run cowan with in36 file 
        if False:
            run_shell_script()

            # rename the files to txt files with index
            totxt(m,"IN36")
            totxt(m,"ING11")
            totxt(m,"OUT2")
            totxt(m,"OUT36")


main()