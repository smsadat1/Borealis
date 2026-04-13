# API Referrence

This document describes the public API exposed by the execution platform.

The API allows clients to submit code, track execution, retrieve results and stream live execution status updates.


## Execution Model

Each execution request is assigned a unique `exec_id`

All operations (status, results, cancellation, streaming) are tied to this identifier.


## POST /execute/

Submit a new code execution request.

``` 
{
 "language": "Python",
 "version": "python 3.10",
 "code_file": "main.py",
 "testcases": [
     {
      "inputs": "...",
      "output": "...",
     }
 ]
}
 ```

Execution response.
```
{
 "exec_id": "abc123",
 "status": "queued",
}
```

## GET /execute/{exec_id}
Response:
```
{
 "exec_id": "abc123",
 "status": "done",
 "results: [
  {
   "testcase": 1,
   "expected": "...",
   "recieved": "...",
   "passed": true,
   "time_ms": "...",
  }
 ]
}
```

## DELETE /execute/{exec_id}
Response:
```
[
 {
  "exec_id": "abc123",
  "status": "cancelled",
 }
]
```


## GET /execute/
Response:
```
[
 {
  "exec_id": "abc123",
  "language": "C++,
  "time": "...",
  "created_at": "...",
 }
]
```

## WS /execute/{exec_id}/stream

### Events
The server streams execution state updates:
```
VALIDATED
RECIEVED
QUEUED
RUNNING 
DONE
```

## Execution states
```
VALIDATED -> input verified
RECIEVED -> request accpted
QUEUED -> waiting for runner
RUNNING -> executing inside sandbox
DONE -> completed successfully
FAILED -> runtime or system error
CANCELLED -> execution aborted by user
```

## Design notes

 - All execution flows are identified by a unique `exec_id`
 - Websocket stream provides real-time state transitions
 - APIService acts only as an orchestration layer
 - RunnerService performs all execution work inside isolated environments

