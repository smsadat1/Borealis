from concurrent import futures
import grpc
from rpc import runner_pb2
from rpc import runner_pb2_grpc

from runner.executor import execute_code


class RunnerServicer(runner_pb2_grpc.RunnerServicer):

    def Execute(self, request, context):
        total_tests, passed_tests, failed_tests, timeouts = execute_code(
            request.language,
            request.source_code,
            request.stdins,
            request.version
        )

        return runner_pb2.ExecutionResponse(
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            timeouts=timeouts,
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