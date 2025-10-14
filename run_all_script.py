import subprocess
import sys
import os

def start_process(command, cwd, name, env=None):
    """Start a process and return it, handling errors gracefully."""
    try:
        print(f"Starting {name}...")
        process = subprocess.Popen(command, cwd=cwd, env=env)
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
BDC_DIR = os.path.join(ROOT_DIR, "agents", "brand_data_collector")
RC_DIR = os.path.join(ROOT_DIR, "agents", "rating_calculator")
SUG_DIR = os.path.join(ROOT_DIR, "agents", "suggestion_agent")

# Resolve virtualenv Python executables if present
def resolve_python_for(dir_with_venv: str) -> str:
    venv_python = os.path.join(dir_with_venv, ".venv", "bin", "python")
    return venv_python if os.path.exists(venv_python) else sys.executable

backend_python = resolve_python_for(BACKEND_DIR)
ubt_python = resolve_python_for(UBT_DIR)
rc_python = resolve_python_for(RC_DIR)
bdc_python = resolve_python_for(BDC_DIR)

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

############################################
# Agents
############################################

# Brand Data Collector (Flask) on 5001
bdc_env = os.environ.copy()
bdc_process = start_process([bdc_python, "app.py"], BDC_DIR, "Brand Data Collector (5001)", env=bdc_env)
if bdc_process:
    processes.append(bdc_process)

# Rating Calculator (FastAPI) on 5002
rc_env = os.environ.copy()
rc_env["RATING_CALCULATOR_PORT"] = "5002"
rc_process = start_process([rc_python, "app.py"], RC_DIR, "Rating Calculator (5002)", env=rc_env)
if rc_process:
    processes.append(rc_process)

# User Behavior Tracker (FastAPI) on 5003
ubt_env = os.environ.copy()
ubt_env["PORT"] = "5003"
ubt_env["RELOAD"] = "true"
ubt_process = start_process([ubt_python, "run.py"], UBT_DIR, "User Behavior Tracker (5003)", env=ubt_env)
if ubt_process:
    processes.append(ubt_process)

# Suggestion Agent (FastAPI) on 5004, wire service URLs
sug_env = os.environ.copy()
sug_env["SUGGESTION_AGENT_PORT"] = "5004"
sug_env["BRAND_COLLECTOR_URL"] = "http://localhost:5001"
sug_env["RATING_CALCULATOR_URL"] = "http://localhost:5002"
sug_env["USER_BEHAVIOR_URL"] = "http://localhost:5003"
sug_process = start_process([sys.executable, "agent4_suggestion.py"], SUG_DIR, "Suggestion Agent (5004)", env=sug_env)
if sug_process:
    processes.append(sug_process)

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
