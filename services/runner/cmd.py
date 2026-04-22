import os
import subprocess

from runner.utils import (
    c_cpp_std, compiled_langs, compiler,
    interpreted_langs
)

def run_process(image, cmd, stdin):

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

    # print("CMD:", cmd)
    # print("DOCKER CMD:", docker_cmd)

    result = subprocess.run(
        docker_cmd,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=30
    )

    print(f'Out: {result.stdout}\nErr: {result.stderr}\nRC: {result.returncode}')
    
    return result.stdout, result.stderr, result.returncode


def cmd_init(language, version, job_id, filename, stdins, image):  


    total_tests=0
    passed_tests=0
    failed_tests=0
    timeouts=0

    if language in compiled_langs:

        if language == "C++":
            std_flag = c_cpp_std["C++"][version]
        elif language == "C":
            std_flag = c_cpp_std["C"][version]
        
        file_path = f"/workspace/{job_id}/{filename}"
        out_path = f"/workspace/{job_id}/a.out"

        # compile
        if language in ["C", "C++"]:
            compile = [compiler[language], std_flag, file_path, "-o", out_path]
        else:
            compile = [compiler[language], file_path, "-o", out_path]

        for stdin in stdins:

            total_tests += 1
            stdout, stderr, returncode = run_process(image, compile, stdin)

            if stderr:
                failed_tests += 1
                # send to Kafka
                data = {"output": stdout, "error": stderr, "returncode": returncode}
                # send_result(producer=producer, topic='exec-topic', data=data)

            # run 
            else: 
                if language in ["C", "C++", "Go", "Rust"]:
                    run = [out_path]
                elif language == "Java":
                    workdir = f"/workspace/{job_id}"
                    run = ["java", "-cp", workdir, "Main"]
                elif language == "C#":
                    run = ["mono", out_path]
            
                stdout, stderr, returncode = run_process(image, compile, stdin)

                if stderr:
                    if stderr == "Timeout":
                        timeouts += 1
                    failed_tests += 1
                else:
                    passed_tests += 1

                # send to Kafka
                data = {"output": stdout, "error": stderr, "returncode": returncode}
                # send_result(producer=producer, topic='exec-topic', data=data)

    elif language in interpreted_langs:

        file_path = f"/workspace/{job_id}/{filename}"

        cmd = ["node", f"/workspace/{job_id}/{filename}"]

        for stdin in stdins:

            total_tests += 1
            stdout, stderr, returncode = run_process(image, cmd, stdin)
            # send to Kafka

            if stderr:
                failed_tests += 1
                if stderr == "Timeout":
                    timeouts += 1
            else:
                passed_tests += 1

            data = {"output": stdout, "error": stderr, "returncode": returncode}
            # send_result(producer=producer, topic='exec-topic', data=data)

    return total_tests, passed_tests, failed_tests, timeouts
    

        
