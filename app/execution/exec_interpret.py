import os
import subprocess

async def exec_interpret(command: str, source_code: str, stdin: str, temp_dir: str):
    
    file_path = os.path.join(temp_dir, "main.py")
    with open(file_path, "w") as f:
        f.write(source_code)

    result = subprocess.run(
        [command, file_path],
        input=stdin,
        capture_output=True, text=True, timeout=5,
    )

    stdout = result.stdout
    stderr = result.stderr
    exit_code = result.returncode

    return stdout, stderr, exit_code