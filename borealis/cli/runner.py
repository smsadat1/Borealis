import os
import questionary
import requests
import sys
import threading
import time
import websocket

from utils import available_languages, available_versions, load_api_key, start_spinner, stop_spinner, spinner_thread


def runner():
    
    api_key = load_api_key()

    if api_key is None:
        print("\033[31m!\033[0m No API key found")
        return

    language = questionary.text("Language: ").ask()
    
    if language not in available_languages:
        print("Provided language is unsupported\nSupported languages: ")
        for al in available_languages:
            print(f"{al} ")
        return

    version = questionary.text("Version: ").ask()

    if version not in available_versions[language]:
        print("Provided version of the language is unavailable or invalid\nAvailable versions: ")
        for av in available_versions[language]:
            print(f"{av} ")
        return

    input_files = questionary.path("Input file(s):").ask()
    source_code_file = questionary.path("Code file (e.g., example.py):").ask()

    files = []

    # input files
    if os.path.isdir(input_files):
        for filename in os.listdir(input_files):
            path = os.path.join(input_files, filename)
            if os.path.isfile(path):
                files.append(("inputs", (filename, open(path, "rb"))))
            else:
                files.append(("inputs", (os.path.basename(input_files), open(input_files, "rb"))))

    # code file
    files.append(("file", (os.path.basename(source_code_file), open(source_code_file, "rb"))))


    data = {"language": language, "version": version}

    try:
        response = requests.post(
            "http://localhost:8000/executions",
            files=files, data=data, timeout=5,
            headers={"X-API-key": api_key},
        )

        if response.status_code == 200:
            print(f"\033[32m✔\033[0m Files sent successfully\n\033[37mⓘ\033[0m Execution ID: {response.json()['id']}")
        elif response.status_code == 401:
            print(response.json()['detail'])
            return
        else:
            print(f"\033[31m✘\033[0m Error from server:", response.status_code)
            return

    except requests.exceptions.ConnectionError:
        print("Server unreachable")
        return

    except requests.exceptions.Timeout:
        print("Server timeout")
        return

    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e))
        return

    exec_id = response.json()['id']
    exec_status = response.json()['status']
    ws = websocket.create_connection(f"ws://localhost:8000/executions/{exec_id}/stream")

    print(f"\033[32m✔\033[0m {exec_status}")

    while True:
        msg = ws.recv()

        if msg == "Borealis is working...":
            start_spinner()

        elif msg == "Done":
            stop_spinner.set()
            if spinner_thread:
                spinner_thread.join()

            # extra space to clear previous log
            sys.stdout.write("\r\033[32m✔\033[0m Done                      \n")
            sys.stdout.flush()
            break

    ws.close()

    output = requests.get(
        "http://localhost:8000/executions" + f'/{exec_id}',
        headers={"X-API-key": api_key}
    )


    if output.status_code == 401: 
        print(output.json()['detail'])
        return
    
    # --- Result ---
    status = output.json()['status']
    total_tests = output.json()['total_tests']
    passed_tests = output.json()['passed_tests']
    failed_tests = output.json()['failed_tests']
    timeouts = output.json()['timeouts']

    if status == "completed":
        print("\033[37mⓘ\033[0m Status: Completed")
    elif status == "failed":
        print(f"\033[37mⓘ\033[0m Status: Failed")

    print('\033[1mExecution summary\033[0m')
    print(f'\033[37mⓘ\033[0m Total tests: {total_tests}\n'
          f'\033[32m✔\033[0m Passed: {passed_tests}\n' 
          f'\033[31m✘\033[0m Failed: {failed_tests}\n' 
          f'\033[37m⏱\033[0m Timeouts: {timeouts}')
