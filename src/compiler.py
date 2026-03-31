import os
import subprocess
import tempfile

from vars import jobs


async def exec_c_cpp(command: str, source_code: str, temp_dir: str):
    
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
            # input=stdin.encode("utf-8"),
            capture_output=True, text=True, timeout=5,
        )

    stdout = run_result.stdout
    stderr = run_result.stderr
    exit_code = run_result.returncode

    return stdout, stderr, exit_code


async def exec_python(command: str, source_code: str, temp_dir: str):
    
    file_path = os.path.join(temp_dir, "main.py")
    with open(file_path, "w") as f:
        f.write(source_code)

    result = subprocess.run(
        [command, file_path],
        capture_output=True, text=True, timeout=5,
    )

    stdout = result.stdout
    stderr = result.stderr
    exit_code = result.returncode

    return stdout, stderr, exit_code


async def borealis_compiler(language: str, source_code: str):

    temp_dir = tempfile.mkdtemp(prefix="borealis_exec_")

    if language == "c":
        stdout, stderr, exit_code = await exec_c_cpp(
            command="gcc", temp_dir=temp_dir, source_code=source_code
        )
    
    elif language == "cpp":
        stdout, stderr, exit_code = await exec_c_cpp(
            command="g++", temp_dir=temp_dir, source_code=source_code
        )
        
    elif language == "python":
        stdout, stderr, exit_code = await exec_python(
            command="python3", temp_dir=temp_dir, source_code=source_code
        )
    
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