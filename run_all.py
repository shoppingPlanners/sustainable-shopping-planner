"""
Run All Agents Script
Starts all 4 agents simultaneously in separate processes
"""

import subprocess
import sys
import time
import os
import signal
from typing import List

# ANSI color codes for pretty output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Agent configuration
AGENTS = [
    {
        'name': 'Brand Data Collector',
        'file': 'agents/agent1_brand_collector.py',
        'port': 5001,
        'color': GREEN
    },
    {
        'name': 'Rating Calculator',
        'file': 'agents/agent2_rating_calculator.py',
        'port': 5002,
        'color': BLUE
    },
    {
        'name': 'User Behavior Tracker',
        'file': 'agents/agent3_user_behavior.py',
        'port': 5003,
        'color': YELLOW
    },
    {
        'name': 'Suggestion Agent',
        'file': 'agents/agent4_suggestion.py',
        'port': 5004,
        'color': GREEN
    }
]

processes: List[subprocess.Popen] = []


def print_header():
    """Print welcome header"""
    print(f"\n{BLUE}{'='*70}")
    print("  🌱 Sustainable Shopping Planner - Integrated System")
    print("  Starting All 4 Agents...")
    print(f"{'='*70}{RESET}\n")


def start_agent(agent: dict) -> subprocess.Popen:
    """Start an agent in a separate process"""
    try:
        print(f"{agent['color']}🚀 Starting {agent['name']} on port {agent['port']}...{RESET}")
        
        # Set environment variable for port
        env = os.environ.copy()
        env_var_name = agent['name'].upper().replace(' ', '_') + '_PORT'
        env[env_var_name] = str(agent['port'])
        
        process = subprocess.Popen(
            [sys.executable, agent['file']],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1
        )
        
        time.sleep(1)  # Give it a moment to start
        
        if process.poll() is None:
            print(f"{GREEN}✅ {agent['name']} started successfully{RESET}")
        else:
            print(f"{RED}❌ {agent['name']} failed to start{RESET}")
        
        return process
        
    except Exception as e:
        print(f"{RED}❌ Error starting {agent['name']}: {e}{RESET}")
        return None


def stop_all_agents():
    """Stop all running agents"""
    print(f"\n{YELLOW}🛑 Stopping all agents...{RESET}")
    
    for process in processes:
        if process and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
    
    print(f"{GREEN}✅ All agents stopped{RESET}")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n{YELLOW}Received interrupt signal...{RESET}")
    stop_all_agents()
    sys.exit(0)


def print_status():
    """Print status of all agents"""
    print(f"\n{BLUE}{'='*70}")
    print("  📊 Agent Status")
    print(f"{'='*70}{RESET}\n")
    
    for i, agent in enumerate(AGENTS):
        if i < len(processes) and processes[i] and processes[i].poll() is None:
            status = f"{GREEN}● RUNNING{RESET}"
        else:
            status = f"{RED}● STOPPED{RESET}"
        
        print(f"  {status}  {agent['name']:<30} http://localhost:{agent['port']}")
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"  {GREEN}All agents are running!{RESET}")
    print(f"  {YELLOW}Press Ctrl+C to stop all agents{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")


def print_api_endpoints():
    """Print useful API endpoints"""
    print(f"\n{BLUE}📡 API Endpoints:{RESET}\n")
    
    endpoints = [
        ("Brand Collector", 5001, [
            "GET  /health - Health check",
            "POST /scrape - Scrape a brand website",
            "GET  /brands - Get all brands"
        ]),
        ("Rating Calculator", 5002, [
            "GET  /health - Health check",
            "POST /calculate - Calculate brand rating",
            "GET  /ratings - Get all ratings"
        ]),
        ("User Behavior", 5003, [
            "GET  /health - Health check",
            "POST /track - Track user event",
            "GET  /behavior/patterns/{user_id} - Get patterns"
        ]),
        ("Suggestion Agent", 5004, [
            "GET  /health - Health check",
            "GET  /suggestions/{user_id} - Get suggestions",
            "GET  /trending - Get trending products"
        ])
    ]
    
    for name, port, apis in endpoints:
        print(f"  {GREEN}{name} (:{port}){RESET}")
        for api in apis:
            print(f"    • {api}")
        print()


def main():
    """Main function"""
    global processes
    
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Print header
    print_header()
    
    # Start all agents
    for agent in AGENTS:
        process = start_agent(agent)
        processes.append(process)
        time.sleep(2)  # Stagger startup
    
    # Wait a moment for all agents to initialize
    print(f"\n{YELLOW}⏳ Waiting for all agents to initialize...{RESET}")
    time.sleep(3)
    
    # Print status
    print_status()
    
    # Print API endpoints
    print_api_endpoints()
    
    # Print example usage
    print(f"{BLUE}💡 Example Usage:{RESET}\n")
    print(f"  # Scrape a brand")
    print(f"  curl -X POST http://localhost:5001/scrape \\")
    print(f"    -H 'Content-Type: application/json' \\")
    print(f"    -d '{\"url\": \"https://example.com\", \"brand_name\": \"EcoBrand\"}'")
    print()
    print(f"  # Get suggestions for a user")
    print(f"  curl http://localhost:5004/suggestions/user123")
    print()
    print(f"  # Track user event")
    print(f"  curl -X POST http://localhost:5003/track \\")
    print(f"    -H 'Content-Type: application/json' \\")
    print(f"    -d '{\"user_id\": \"user123\", \"event_type\": \"view\", \"product_id\": \"prod1\"}'")
    print()
    
    # Keep running until interrupted
    try:
        while True:
            time.sleep(1)
            
            # Check if any process has died
            for i, process in enumerate(processes):
                if process and process.poll() is not None:
                    print(f"{RED}⚠️  {AGENTS[i]['name']} has stopped unexpectedly{RESET}")
                    
    except KeyboardInterrupt:
        pass
    finally:
        stop_all_agents()


if __name__ == "__main__":
    main()

