import os
import subprocess

async def exec_code(run_cmd: list[str], language: str, stdin: str, temp_dir: str):
    
    image_map = {
        "python": "borealis-exec-py:latest",
        "c": "borealis-exec-c_cpp:latest",
        "cpp": "borealis-exec-c_cpp:latest",
        "js": "borealis-exec-js:latest",
        "java": "borealis-exec-java:latest",
        "php": "borealis-exec-php:latest",
        "go": "borealis-exec-go:latest",
        "rust": "borealis-exec-rust:latest",
        "c#": "borealis-exec-csharp:latest",
        "ruby": "borealis-exec-ruby:latest",
    }

    docker_cmd = [
        "docker", "run", "--rm", "-i",
        "--runtime=runsc",
        "--network", "none",
        "--cpus", "1",
        "--memory", "128m",
        "--pids-limit", "64",
        "--security-opt", "no-new-privileges=false",
        "--user", "1000:1000",
        "-v", f"{temp_dir}:/workspace",
        image_map[language],
    ] + run_cmd

    result = subprocess.run(
        docker_cmd,
        input=stdin,
        capture_output=True, text=True, timeout=10
    )

    stdout = result.stdout
    stderr = result.stderr
    exit_code = result.returncode

    return stdout, stderr, exit_code