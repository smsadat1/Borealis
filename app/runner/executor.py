import subprocess
import uuid
import os

from runner.cmd import cmd_init
from runner.utils import image_map

import subprocess
import uuid
import os


def execute_code(language: str, code: str, stdin: str, version: str):
    
    job_id = uuid.uuid4().hex
    job_dir = os.path.abspath(f"/var/borealis/jobs/{job_id}")
    os.makedirs(job_dir, exist_ok=True)

    print(f"Lang: {language} | Ver: {version}")

    file_map = {
        "C": "main.c",
        "C++": "main.cpp",
        "C#": "main.cs",
        "Java": "Main.java",
        "Go": "main.go",
        "Javascript": "main.js",
        "PHP": "main.php",
        "Python": "main.py",
        "Ruby": "main.rb",
        "Rust": "main.rs",
    }

    filename = file_map.get(language)
    if not filename:
        return "", "Unsupported language", 1

    file_path = os.path.join(job_dir, filename)

    with open(file_path, "w") as f:
        f.write(code)
        f.flush()
        os.fsync(f.fileno())

    print("HOST VIEW:")
    print(os.listdir(job_dir))

    image = image_map[version]

    # =========================
    # COMMAND PER LANG
    # =========================

    c_cpp_std = {
        'C': {
            'C99': '-std=c99',
            'C11': '-std=c11',
            'C17': '-std=gnu17'
        },
        'C++': {
            'C++11': '-std=c++11',
            'C++17': '-std=c++17',
            'C++20': '-std=c++20',
        }
    }

    if language == "C++":
        std_flag = c_cpp_std["C++"][version]
        file_path = f"/workspace/{job_id}/{filename}"
        out_path = f"/workspace/{job_id}/a.out"

        compile = ["g++", std_flag, file_path, "-o", out_path]
        _, stderr, returncode = cmd_init(image=image, cmd=compile, stdin="")

        if returncode != 0:
            return "", stderr, returncode

        run = [out_path]
        stdout, stderr, returncode = cmd_init(image=image, cmd=run, stdin=stdin)
    

    elif language == "C":
        std_flag = c_cpp_std["C"][version]
        file_path = f"/workspace/{job_id}/{filename}"
        out_path = f"/workspace/{job_id}/a.out"

        compile = ["gcc", std_flag, file_path, "-o", out_path]
        _, stderr, returncode = cmd_init(image=image, cmd=compile, stdin="")

        if returncode != 0:
            return "", stderr, returncode

        run = [out_path]
        stdout, stderr, returncode = cmd_init(image=image, cmd=run, stdin=stdin)

    elif language == "C#":
        file_path = f"/workspace/{job_id}/{filename}"
        out_path = f"/workspace/{job_id}/a.out"

        compile = ["mcs", file_path, f"-out:{out_path}"]
        stdout, stderr, returncode = cmd_init(image=image, cmd=compile, stdin="")

        if returncode != 0:
            return stdout, stderr, returncode

        run = ["mono", out_path]
        stdout, stderr, returncode = cmd_init(image=image, cmd=run, stdin=stdin)

    elif language == "Rust":
        file_path = f"/workspace/{job_id}/{filename}"
        out_path = f"/workspace/{job_id}/a.out"

        compile = ["rustc", file_path, "-o", out_path]
        _, stderr, returncode = cmd_init(image=image, cmd=compile, stdin="")

        if returncode != 0:
            return "", stderr, returncode

        run = [out_path]
        stdout, stderr, returncode = cmd_init(image=image, cmd=run, stdin=stdin)

    elif language == "Java":
        file_path = f"/workspace/{job_id}/{filename}"
        workdir = f"/workspace/{job_id}"

        compile = ["javac", file_path]
        _, stderr, returncode = cmd_init(image=image, cmd=compile, stdin="")

        if returncode != 0:
            return "", stderr, returncode

        # assuming Main.java → class Main
        run = ["java", "-cp", workdir, "Main"]
        stdout, stderr, returncode = cmd_init(image=image, cmd=run, stdin=stdin)

    elif language == "Javascript":
        cmd = ["node", f"/workspace/{job_id}/{filename}"]
        stdout, stderr, returncode = cmd_init(image=image, cmd=cmd, stdin=stdin)

    elif language == "Python":
        cmd = ["python3", f"/workspace/{job_id}/{filename}"]
        stdout, stderr, returncode = cmd_init(image=image, cmd=cmd, stdin=stdin)

    elif language == "Ruby":
        cmd = ["ruby", f"/workspace/{job_id}/{filename}"]
        stdout, stderr, returncode = cmd_init(image=image, cmd=cmd, stdin=stdin)

    elif language == "PHP":
        cmd = ["php", f"/workspace/{job_id}/{filename}"]
        stdout, stderr, returncode = cmd_init(image=image, cmd=cmd, stdin=stdin)

    elif language == "Go":
        file_path = f"/workspace/{job_id}/{filename}"
        out_path = f"/workspace/{job_id}/a.out"

        compile = ["go", "build", "-o", out_path, file_path]
        _, stderr, returncode = cmd_init(image=image, cmd=compile, stdin="")

        if returncode != 0:
            return "", stderr, returncode

        run = [out_path]
        stdout, stderr, returncode = cmd_init(image=image, cmd=run, stdin=stdin)

    else:
        return "", "Unsupported language", 1

    return stdout, stderr, returncode