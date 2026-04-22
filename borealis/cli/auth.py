import os
import json
import questionary
import requests

from utils import CONFIG_DIR, CONFIG_FILE, load_api_key


def save_api_key(key):
    
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": key}, f, indent=4)


def mask_key(key):
    return key[:4] + "****" + key[-4:]


def prompt_choice():
    
    choice = questionary.select(
        "API key not found. What do you want to do?",
        choices=[
            "Generate new key",
            "Use existing key"
        ]
    ).ask()

    return choice



def generate_new_key():
    
    print("\nGenerating new API key...")

    new_key = requests.post("http://localhost:7000/keygen")
    save_api_key(new_key.json()['api_key'])
    print("\033[32m✔\033[0m New API key saved!")



def use_existing_key():
    key = input("\nEnter your API key: ").strip()

    if not key:
        print("\033[31m⨉\033[0m Invalid key")
        return
    
    data = {"api_key": key}
    validate_key = requests.post("http://localhost:7000/validate", json=data)

    if validate_key.status_code == 200: 
        print("\033[32m✔\033[0m " + validate_key.json()['message'])
        save_api_key(key)
        print("\033[32m✔\033[0m API key saved!")
    else:
        print("\033[31m⨉\033[0m " + validate_key.json()['message'])
        


def login():
    api_key = load_api_key()

    if api_key:
       print("\033[32m✔\033[0m Already logged in")
       print(f"API Key: {mask_key(api_key)}")
       return

    choice = prompt_choice()

    if choice == "Generate new key":
        generate_new_key()
    elif choice == "Use existing key":
        use_existing_key()
