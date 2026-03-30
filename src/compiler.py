import os
import subprocess
import tempfile

from vars import jobs

async def borealis_compiler(language: str, source_code: str):

    temp_dir = tempfile.mkdtemp(prefix="borealis_exec_")

    if language == "c":
        command = "gcc"
        file_path = os.path.join(temp_dir, "main.c")

    elif language == "cpp":
        command = "g++"
        file_path = os.path.join(temp_dir, "main.cpp")

    elif language == "python":
        command = "python3"
        file_path = os.path.join(temp_dir, "main.py")


    with open(file_path, "w") as f:
        f.write(source_code)

    result = subprocess.run(
        [command, file_path],
        capture_output=True,
        text=True, 
        timeout=5,
    )

    stdout = result.stdout
    stderr = result.stderr
    exit_code = result.returncode

    return stdout, stderr, exit_code


async def run_borealis(exec_id, lang, src_code):

    stdout, stderr, exit_code = await borealis_compiler(language=lang, source_code=src_code)

    # save result
    jobs[exec_id].update({
        "status": "completed",
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
    })