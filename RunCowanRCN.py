import subprocess
import os

# Get the directory where the Python script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the shell script (port.sh) in the same directory
port_script = os.path.join(script_dir, "port.sh")

# Full path to bash.exe (Git Bash on Windows)
bash_path = "C:\\Program Files\\Git\\bin\\bash.exe"

# Function to run the shell script
def run_shell_script():
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

# Call the function to run the shell script
run_shell_script()