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
        version = request.version
        code = request.source_code
        stdin = request.stdin or ""
        exec_id = request.exec_id


        print(f"[Runner] Received job: lang={language}, code length={len(code)}, stdin={len(stdin)}")

        if language == "C":
            filename = "code.c"
        elif language == "C++":
            filename = "code.cpp"
        elif language == "Javascript":
            filename = "code.js"
        elif language == "Python":
            filename = "code.py"
        elif language == "Java":
            filename = "code.java"
        elif language == "PHP":
            filename = "code.php"
        elif language == "Ruby":
            filename = "code.rb"
        elif language == "Rust":
            filename = "code.rs"
        elif language == "C#":
            filename = "code.cs"
        elif language == "Go":
            filename = "code.go"
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
            if language == "Python":
                run_cmd = ["python", f"/workspace/{filename}"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(run_cmd, version=version, stdin=stdin, temp_dir=job_dir)

            elif language == "Javascript":
                run_cmd = ["node", f"/workspace/{filename}"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(run_cmd, version=version, stdin=stdin, temp_dir=job_dir)

            elif language == "Java":
                # Compile then run
                run_cmd = ["sh", "-c", f"javac /workspace/{filename} && java -cp /workspace {filename[:-5]}"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(run_cmd, version=version, stdin=stdin, temp_dir=job_dir)

            elif language == "PHP":
                run_cmd = ["php", f"/workspace/{filename}"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(run_cmd, version=version, stdin=stdin, temp_dir=job_dir)

            elif language == "Ruby":
                run_cmd = ["ruby", f"/workspace/{filename}"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(run_cmd, version=version, stdin=stdin, temp_dir=job_dir)

            elif language == "Rust":
                # Compile Rust to binary then execute
                run_cmd = ["sh", "-c", f"rustc /workspace/{filename} -o /workspace/a.out && /workspace/a.out"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(run_cmd, version=version, stdin=stdin, temp_dir=job_dir)

            elif language == "C#":
                # Using mcs (Mono C# compiler) then run via mono
                run_cmd = ["sh", "-c", f"mcs /workspace/{filename} -out:/workspace/a.exe && mono /workspace/a.exe"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(run_cmd, version=version, stdin=stdin, temp_dir=job_dir)

            elif language == "Go":
                # Go compile then run
                run_cmd = ["sh", "-c", f"go build -o /workspace/a.out /workspace/{filename} && /workspace/a.out"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(run_cmd, version=version, stdin=stdin, temp_dir=job_dir)


            elif language in ["C", "C++"]:
                # Step 1: compile
                compile_cmd = ["gcc" if language == "c" else "g++", f"/workspace/{filename}", "-o", "/workspace/a.out"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(compile_cmd, version=version, stdin="", temp_dir=job_dir)
                if exit_code != 0:
                    await self.safe_update_status(runner_pb2.StatusUpdate(exec_id=exec_id, status="CompileError"))
                    return runner_pb2.ExecutionResponse(stdout=stdout, stderr=stderr, exit_code=exit_code, exec_id=exec_id)

                # Step 2: run
                run_cmd = ["/workspace/a.out"]
                print(f"Job dir contents: {os.listdir(job_dir)}")
                stdout, stderr, exit_code = await exec_code(run_cmd, version=version, stdin=stdin, temp_dir=job_dir)

            else:
                return runner_pb2.ExecutionResponse(
                    stdout="",
                    stderr="Unsupported language",
                    exit_code=1,
                    exec_id=exec_id,
                )
                
            stdout = str(stdout or "")
            stderr = str(stderr or "")
            exit_code = int(exit_code or 1)

            print(f"[Runner] Finished job: lang={language}, output length={len(stdout)}, error lenghth={len(stderr)}, exit code={exit_code}")

            return runner_pb2.ExecutionResponse(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                exec_id=exec_id,
            )
            
        except subprocess.TimeoutExpired:
            return runner_pb2.ExecutionResponse(stdout="", stderr="Timeout", exit_code=124, exec_id=exec_id)

        except Exception as e:
            # Catch everything to prevent INTERNAL errors
            return runner_pb2.ExecutionResponse(stdout="", stderr=str(e), exit_code=1, exec_id=exec_id)
        
    async def close(self):
        print("Closing grpc server at port 50051")
        await self.channel.close()


async def serve():
    server = aio.server(futures.ThreadPoolExecutor(max_workers=4)) 
    servicer = RunnerServicer()
    runner_pb2_grpc.add_RunnerServicer_to_server(servicer, server)

    server.add_insecure_port('0.0.0.0:50051')
    await server.start()
    print("gRPC server running on port 50051")

    try:
        await server.wait_for_termination()
    finally:
        await servicer.close()

if __name__ == "__main__":
    asyncio.run(serve())