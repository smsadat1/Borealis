import json
from grpc import aio

from rpc.auth_pb2_grpc import AuthStub
from rpc import runner_pb2
from rpc.runner_pb2_grpc import RunnerStub

from api.ws import send_status


async def run_borealis(request, exec_id, lang, version, src_code, stdin):
    
    redis = request.app.state.redis

    await send_status(exec_id=exec_id, status="Borealis is working...")

    # create async channel
    async with aio.insecure_channel("runner:50051") as channel:

        runner_stub = RunnerStub(channel)

        try:
            # Await the Execute coroutine directly
            response = await runner_stub.Execute(
                runner_pb2.ExecutionRequest(
                    language=lang,
                    version=version,
                    source_code=src_code,
                    stdin=stdin or "",
                    exec_id=exec_id,
                )
            )


            job_data = {
                "id": exec_id,
                "status": "completed",
                "stdout": response.stdout,
                "stderr": response.stderr,
                "exit_code": response.exit_code
            }

        except Exception as e:
            job_data = {
                "id": exec_id,
                "status": "failed",
                "stdout": "",
                "stderr": str(e),
                "exit_code": 1
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