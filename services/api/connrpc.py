import json
from grpc import aio
import traceback

from api.ws import send_status
from rpc.auth_pb2_grpc import AuthStub
from rpc import runner_pb2
from rpc.runner_pb2_grpc import RunnerStub


async def run_borealis(request, exec_id, lang, version, src_code, stdins: list[str]):
    
    redis = request.app.state.redis

    await send_status(exec_id=exec_id, status="Borealis is working...")

    # create async channel
    async with aio.insecure_channel("runner:50051") as channel:

        runner_stub = RunnerStub(channel)

        # after connecting gRPC

        try:
            # Await the Execute coroutine directly
            response = await runner_stub.Execute(
                runner_pb2.ExecutionRequest(
                    language=lang,
                    version=version,
                    source_code=src_code,
                    stdins=stdins or [],
                    exec_id=exec_id,
                )
            )

            job_data = {
                "id": exec_id,
                "status": "completed",
                "total_tests": response.total_tests,
                "passed_tests": response.passed_tests,
                "failed_tests": response.failed_tests,
                "timeouts": response.timeouts,
            }

        except Exception as e:
            print("Execution failed:", repr(e))
            traceback.print_exc()
            job_data = {
                "id": exec_id,
                "status": "failed",
                "total_tests": -1,
                "passed_tests": -1,
                "failed_tests": -1,
                "timeouts": -1,
            }

        # Store result in Redis
        await redis.set(f"exec_id:{exec_id}", json.dumps(job_data))
        print(f"[API] Job {exec_id} saved to Redis with status: {job_data['status']}")
        await send_status(exec_id=exec_id, status="Done")


class AuthClient:

     def __init__(self):
        self.channel = aio.insecure_channel("auth-grpc:50053")
        self.stub = AuthStub(self.channel)

auth_client = AuthClient()