# Run this script in command line with $ python run_python_files.py
import subprocess

def run_script(script_path):
    subprocess.run(["python", script_path])

def main():
    # Specify the path to your Python script
    script_path = "prepare_run_files.py"
    
    # Run the script
    run_script(script_path)

if __name__ == "__main__":
    main()
