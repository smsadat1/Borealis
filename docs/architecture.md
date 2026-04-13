# Execution Flow

This document describes the end-to-end lifecycle of a code execution request, from client submission to final output response.


## High-Level Flow

    1. Client submits code via API or CLI
    2. APIService validates request and API key
    3. APIService forwards execution request to RunnerService via gRPC
    4. RunnerService selects appropriate runtime environment
    5. Code is executed inside an isolated container
    6. Output and metadata are returned to APIService
    7. APIService sends final response to client

```
Client
  ↓
APIService (Starlette) <- AuthService (API key validation)
  ↓ gRPC
RunnerService
  ↓
Container (gVisor sandbox)
  ↓
Execution Output
  ↑
APIService
  ↑
Client
```



## Execution Model

Currently, execution is synchronous:
- API waits for RunnerService response before returning result

Future improvements may include:
- async job queue
- WebSocket-based streaming output


## Service Responsibilities

- APIService → request handling, validation, response formatting
- AuthService → authentication and API key management
- RunnerService → execution orchestration and sandbox management


## Design Goal

The execution flow is designed to isolate responsibilities and ensure that untrusted code execution is fully separated from request handling and authentication logic.