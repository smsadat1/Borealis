from concurrent import futures
import grpc
from rpc import runner_pb2
from rpc import runner_pb2_grpc

from runner.executor import execute_code


class RunnerServicer(runner_pb2_grpc.RunnerServicer):

    def Execute(self, request, context):
        stdout, stderr, code = execute_code(
            request.language,
            request.source_code,
            request.stdin,
            request.version
        )

        return runner_pb2.ExecutionResponse(
            stdout=stdout,
            stderr=stderr,
            exit_code=code
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    runner_pb2_grpc.add_RunnerServicer_to_server(RunnerServicer(), server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("[RUNNER] grpc server started in port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()