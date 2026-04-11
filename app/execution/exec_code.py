import os
import subprocess

async def exec_code(run_cmd: list[str], version: str, stdin: str, temp_dir: str):
    
    image_map = {
        "Python 3.8": "borealis-exec-py-3-8:latest",
        "Python 3.10": "borealis-exec-py-3-10:latest",
        "Python 3.12": "borealis-exec-py-3-12:latest",
        "C11": "borealis-exec-c-cpp:latest",
        "C17": "borealis-exec-c_cpp:latest",
        "C99": "borealis-exec-c_cpp:latest",
        "C++11": "borealis-exec-c_cpp:latest",
        "C++17": "borealis-exec-c_cpp:latest",
        "C++20": "borealis-exec-c_cpp:latest",
        "Node 14": "borealis-exec-js-node-20:latest",
        "Node 18": "borealis-exec-js-node-18:latest",
        "Node 20": "borealis-exec-js-node-20:latest",
        "Java 8": "borealis-exec-java-8:latest",
        "Java 11": "borealis-exec-java-11:latest",
        "Java 17": "borealis-exec-java-17:latest",
        "PHP 7.4": "borealis-exec-php-7.4:latest",
        "PHP 8.0": "borealis-exec-php-8.0:latest",
        "PHP 8.2": "borealis-exec-php-8.2:latest",
        "Go 1.18": "borealis-exec-go-1.18:latest",
        "Go 1.20": "borealis-exec-go-1.20:latest",
        "Go 1.22": "borealis-exec-go-1.22:latest",
        "Rust 1.60": "borealis-exec-rust-1.60:latest",
        "Rust 1.70": "borealis-exec-rust-1.70:latest",
        "Rust 1.75": "borealis-exec-rust-1.75:latest",
        ".NET 6": "borealis-exec-csharp-6:latest",
        ".NET 7": "borealis-exec-csharp-7:latest",
        ".NET 8": "borealis-exec-csharp-8:latest",
        "Ruby 2.7": "borealis-exec-ruby-2.7:latest",
        "Ruby 3.0": "borealis-exec-ruby-3.0:latest",
        "Ruby 3.2": "borealis-exec-ruby-3.2:latest",
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
        image_map[version],
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