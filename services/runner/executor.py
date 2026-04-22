import os
import uuid

from runner.cmd import cmd_init
from runner.utils import image_map


def execute_code(language: str, code: str, stdins: list[str], version: str):
    
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

    totaltests, passed_tests, failed_tests, timeouts = cmd_init(language, version, job_id, filename, stdins, image)

    return totaltests, passed_tests, failed_tests, timeouts