import os
import subprocess

async def exec_compile(command: str, source_code: str, stdin: str, temp_dir: str):
    
    file_path = os.path.join(temp_dir, "main.cpp")
    with open(file_path, "w") as f:
        f.write(source_code)
    
    compiled_result = subprocess.run(
        [command, file_path, "-o", os.path.join(temp_dir, "a.out")],
        capture_output=True, text=True,
    )

    if compiled_result.returncode != 0:
        # compilation failed
        stdout = compiled_result.stdout
        stderr = compiled_result.stderr
    else:
        # execute binary
        run_result = subprocess.run(
            [os.path.join(temp_dir, "a.out")],
            input=stdin,
            capture_output=True, text=True, timeout=5,
        )

    stdout = run_result.stdout
    stderr = run_result.stderr
    exit_code = run_result.returncode

    return stdout, stderr, exit_code