import os
import subprocess

def cmd_init(image, cmd, stdin):
    
    docker_cmd = [
        "docker", "run", "--rm", "-i",
        "--runtime=runsc",
        "--network", "none",
        "--cpus", "1",
        "--memory", "1024m",
        "--pids-limit", "512",
        "--security-opt", "no-new-privileges=false",
        "--user", f"{os.getuid()}:{os.getgid()}",
        "-v", "/var/borealis/jobs:/workspace",
        image,
        *cmd
    ]

    print("CMD:", cmd)
    print("DOCKER CMD:", docker_cmd)

    result = subprocess.run(
        docker_cmd,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=30
    )

    return result.stdout, result.stderr, result.returncode