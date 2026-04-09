import asyncio
from grpc import aio
from concurrent import futures
import subprocess

import uuid
import os

from rpc import runner_pb2
from rpc import runner_pb2_grpc

from execution.exec_code import exec_code

class RunnerServicer(runner_pb2_grpc.RunnerServicer):

    async def Execute(self, request, context):
        language = request.language
        code = request.source_code
        stdin = request.stdin or ""

        print(f"[Runner] Received job: lang={language}, code length={len(code)}, stdin={len(stdin)}")

        if language == "js":
            filename = "code.js"
        elif language == "python":
            filename = "code.py"
        elif language in ["c", "cpp"]:
            filename = "code.c" if language == "c" else "code.cpp"
        else:
            return runner_pb2.ExecutionResponse(
                stdout="",
                stderr=f"Unsupported language: {language}",
                exit_code=1
            )

        job_dir = f"/tmp/borealis_jobs/{uuid.uuid4().hex}"
        os.makedirs(job_dir, exist_ok=True)
        os.chown(job_dir, 1000, 1000)  # give ownership to UID 1000
        os.chmod(job_dir, 0o777)  # give write access
        file_path = os.path.join(job_dir, filename)

        # Write file and flush to ensure content is on disk
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
            f.flush()
            os.fsync(f.fileno())

        # Check contents immediately [DEBUG]
        # print(f"Job dir contents: {os.listdir(job_dir)}")
        # for fname in os.listdir(job_dir):
        #     fpath = os.path.join(job_dir, fname)
        #     if os.path.isfile(fpath):
        #         with open(fpath, "r", encoding="utf-8") as f:
        #             contents = f.read()
        #         print(f"\n--- {fname} ---\n{contents}\n--- end of {fname} ---")

            
            try:
                if language == "python":
                    run_cmd = ["python", f"/workspace/{filename}"]
                    print(f"Job dir contents: {os.listdir(job_dir)}")
                    stdout, stderr, exit_code = await exec_code(run_cmd, language="python", stdin=stdin, temp_dir=job_dir)

                elif language == "js":
                    run_cmd = ["node", f"/workspace/{filename}"]
                    print(f"Job dir contents: {os.listdir(job_dir)}")
                    stdout, stderr, exit_code = await exec_code(run_cmd, language="js", stdin=stdin, temp_dir=job_dir)

                elif language in ["c", "cpp"]:
                    # Step 1: compile
                    compile_cmd = ["gcc" if language == "c" else "g++", f"/workspace/{filename}", "-o", "/workspace/a.out"]
                    print(f"Job dir contents: {os.listdir(job_dir)}")
                    stdout, stderr, exit_code = await exec_code(compile_cmd, language=language, stdin="", temp_dir=job_dir)
                    if exit_code != 0:
                        return runner_pb2.ExecutionResponse(stdout=stdout, stderr=stderr, exit_code=exit_code)

                    # Step 2: run
                    run_cmd = ["/workspace/a.out"]
                    print(f"Job dir contents: {os.listdir(job_dir)}")
                    stdout, stderr, exit_code = await exec_code(run_cmd, language=language, stdin=stdin, temp_dir=job_dir)

                else:
                    return runner_pb2.ExecutionResponse(
                        stdout="",
                        stderr="Unsupported language",
                        exit_code=1
                    )
                
                stdout = str(stdout or "")
                stderr = str(stderr or "")
                exit_code = int(exit_code or 1)

                print(f"[Runner] Finished job: lang={language}, output length={len(stdout)}, error lenghth={len(stderr)}, exit code={exit_code}")

                return runner_pb2.ExecutionResponse(
                    stdout=stdout,
                    stderr=stderr,
                    exit_code=exit_code,
                )

            except subprocess.TimeoutExpired:
                return runner_pb2.ExecutionResponse(
                    stdout="",
                    stderr="Timeout",
                    exit_code=124
                )
            
            except Exception as e:
                # Catch everything to prevent INTERNAL errors
                return runner_pb2.ExecutionResponse(
                    stdout="",
                    stderr=f"Runner exception: {str(e)}",
                    exit_code=1
                )


async def serve():
    server = aio.server(futures.ThreadPoolExecutor(max_workers=4)) 
    runner_pb2_grpc.add_RunnerServicer_to_server(RunnerServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("gRPC server running on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())