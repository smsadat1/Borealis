import json
from pathlib import Path
import sys
import itertools
import threading
import time


stop_spinner = threading.Event()
spinner_thread = None

def start_spinner():
    global spinner_thread

    if spinner_thread and spinner_thread.is_alive():
        return  # already running

    stop_spinner.clear()
    spinner_thread = threading.Thread(target=spinner, daemon=True)
    spinner_thread.start()


available_languages = [
    "C", "C++", "C#", "Go", "Java", 
    "Javascript", "PHP", "Python", "Ruby", "Rust"
]

available_versions = {
    "C": ["C11", "C17", "C99"],
    "C++": ["C++11", "C++17", "C++20"],
    "C#": [".NET6", ".NET7", ".NET8"],
    "Go": ["Go1.18", "Go1.20", "Go1.22"],
    "Java": ["Java8", "Java11", "Java17"],
    "Javascript": ["Node14", "Node18", "Node20"],
    "PHP": ["PHP7.4", "PHP8.0", "PHP8.2"],
    "Python": ["Python3.8", "Python3.10", "Python3.12"],
    "Ruby": ["Ruby2.7", "Ruby3.0", "Ruby3.2"],
    "Rust": ["Rust1.60", "Rust1.70", "Rust1.75"],
}


CONFIG_DIR = Path.home()/".borealis"
CONFIG_FILE = CONFIG_DIR/"config.json"


def load_api_key():
    
    if not CONFIG_FILE.exists():
        return None 
    
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("api_key")
    except Exception:
        return None

def spinner():
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

    i = 0
    while not stop_spinner.is_set():
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r\033[33m{frame}\033[0m Borealis is working...")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1

    sys.stdout.write("\r\033[2K\033[32m\033[0m\n")
    sys.stdout.flush()
