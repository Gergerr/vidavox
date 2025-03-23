# run_all.py
import multiprocessing
import subprocess
import os
import time
import random

# List of scripts to run
scripts = [
    "appendix.py",
    "generate_operation.py",
    "getting_started.py",
    "intro.py",
    "safety.py",
    "specs.py",
    "troubleshooting.py",
    "warranty.py"
]

def run_script(script_name):
    """Fungsi untuk menjalankan satu skrip."""
    time.sleep(random.uniform(3, 5))  
    print(f"Starting {script_name}...")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{script_name} completed successfully.")
    else:
        print(f"Error in {script_name}: {result.stderr}")

if __name__ == "__main__":
    # Pastikan di direktori yang benar
    os.chdir("/Users/geraldo/Documents/Code/Vidavox/vidavox/synthetic-pdf")
    
    # Buat pool proses
    pool = multiprocessing.Pool(processes=len(scripts))  # Jumlah proses sesuai jumlah skrip
    pool.map(run_script, scripts)
    pool.close()
    pool.join()
    
    print("All scripts have finished running.")