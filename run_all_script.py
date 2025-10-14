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

# Start all processes
processes = []

# Start frontend
frontend_process = start_process(["npm", "run", "dev"], "frontend", "Frontend")
if frontend_process:
    processes.append(frontend_process)

# Start backend
backend_process = start_process(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"], "backend/src", "Backend")
if backend_process:
    processes.append(backend_process)

# Start user behavior tracker agent
agent_process = start_process(["python", "run.py"], "agents/user_behavior_tracker", "User Behavior Tracker")
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
