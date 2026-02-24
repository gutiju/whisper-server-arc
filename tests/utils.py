import socket
import subprocess
import os
import time

def is_server_running(host="127.0.0.1", port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def ensure_server_running():
    """Returns (process, started_by_us)"""
    if is_server_running():
        return None, False

    print("Server not running. Launching...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    # Use venv python to match requirements
    python_exe = os.path.join(root_dir, "venv", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        python_exe = os.path.join(root_dir, ".venv", "Scripts", "python.exe")
    
    if not os.path.exists(python_exe):
         python_exe = "python"
         
    server_process = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=root_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait for server to start
    print("Waiting for server to initialize (this can take up to 60s)...")
    max_retries = 15
    for i in range(max_retries):
        time.sleep(5)
        if is_server_running():
            print("Server port is open.")
            # Give it another few seconds to be fully ready (FastAPI startup events)
            time.sleep(2)
            return server_process, True
        print(f"  Retry {i+1}/{max_retries}...")
    
    print("❌ Error: Server failed to start in time.")
    server_process.terminate()
    return None, False
