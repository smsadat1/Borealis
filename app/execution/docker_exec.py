import asyncio
from grpc import aio
from concurrent import futures
import subprocess

import tempfile
import os

from rpc import runner_pb2
from rpc import runner_pb2_grpc

from execution.exec_compile import exec_compile
from execution.exec_interpret import exec_interpret

class RunnerServicer(runner_pb2_grpc.RunnerServicer):

    async def Execute(self, request, context):
        language = request.language
        code = request.source_code
        stdin = request.stdin or ""

        print(f"[Runner] Received job: lang={language}, code length={len(code)}, stdin={len(stdin)}")

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'code')

            with open(file_path, "w") as f:
                f.write(code)

            try:
                if language == "python":
                    stdout, stderr, exit_code = await exec_interpret("python", source_code=code, stdin=stdin, temp_dir=tmpdir)

                elif language == "cpp":
                    stdout, stderr, exit_code = await exec_compile("g++", source_code=code, stdin=stdin, temp_dir=tmpdir)

                elif language == "c":
                    stdout, stderr, exit_code = await exec_compile("gcc", source_code=code, stdin=stdin, temp_dir=tmpdir)

                elif language == "js":
                    stdout, stderr, exit_code = await exec_interpret("node", source_code=code, stdin=stdin, temp_dir=tmpdir)

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