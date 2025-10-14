import subprocess
import sys
import os

def start_process(command, cwd, name):
    """Start a process and return it, handling errors gracefully."""
    try:
        print(f"Starting {name}...")
        process = subprocess.Popen(command, cwd=cwd)
        print(f"{name} started with PID {process.pid}")
        return process
    except FileNotFoundError as e:
        print(f"Error starting {name}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error starting {name}: {e}")
        return None

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Resolve absolute working directories
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
BACKEND_SRC_DIR = os.path.join(BACKEND_DIR, "src")
UBT_DIR = os.path.join(ROOT_DIR, "agents", "user_behavior_tracker")

# Resolve virtualenv Python executables if present
def resolve_python_for(dir_with_venv: str) -> str:
    venv_python = os.path.join(dir_with_venv, ".venv", "bin", "python")
    return venv_python if os.path.exists(venv_python) else sys.executable

backend_python = resolve_python_for(BACKEND_DIR)
ubt_python = resolve_python_for(UBT_DIR)

# Start all processes
processes = []

# Start frontend (uses system Node in PATH)
frontend_process = start_process(["npm", "run", "dev"], FRONTEND_DIR, "Frontend")
if frontend_process:
    processes.append(frontend_process)

# Start backend with its venv Python via uvicorn on 0.0.0.0:8000
backend_process = start_process([
    backend_python,
    "-m",
    "uvicorn",
    "main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000",
    "--reload",
], BACKEND_SRC_DIR, "Backend")
if backend_process:
    processes.append(backend_process)

# Start user behavior tracker agent with its venv Python
agent_process = start_process([ubt_python, "run.py"], UBT_DIR, "User Behavior Tracker")
if agent_process:
    processes.append(agent_process)

if not processes:
    print("No processes started successfully. Exiting.")
    sys.exit(1)

print(f"\nStarted {len(processes)} processes. Press Ctrl+C to stop all processes.\n")

try:
    # Wait for all processes
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("\nShutting down all processes...")
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=5)  # Wait up to 5 seconds for graceful shutdown
        except subprocess.TimeoutExpired:
            print(f"Force killing process {p.pid}")
            p.kill()
        except Exception as e:
            print(f"Error stopping process {p.pid}: {e}")
    print("All processes stopped.")
