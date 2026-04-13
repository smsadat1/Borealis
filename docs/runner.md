# RunnerService

RunnerService is responsible for executing untrusted user-submitted code inside isolated environments with strict resource and security constraints.


## Responsibilities

- Selecting appropriate runtime (language + version)
- Spawning isolated execution containers
- Enforcing resource limits
- Capturing execution output
- Cleaning up execution environments


## Runtime System

Each execution request specifies:
- programming language
- version (e.g., Python 3.10, C++20)

RunnerService maps this to a prebuilt container image:
- python:3.10 → image A
- cpp:20 → image B


## Execution Pipeline

1. Receive execution request via gRPC
2. Validate request payload
3. Select runtime image
4. Create container with restrictions
5. Mount code and testcases
6. Execute entrypoint command
7. Capture stdout, stderr, exit code
8. Destroy container
9. Return structured result


## Isolation Layer

Execution is performed using:
- Docker containers
- gVisor (runsc) as runtime sandbox

Each container is:
- ephemeral
- stateless
- fully destroyed after execution


## Resource Limits

Each execution is restricted by:

- CPU time limit
- Memory limit
- Execution timeout
- No network access
- No privileged syscalls


## Output Model

RunnerService captures:

- Standard Output (stdout)
- Standard Error (stderr)
- Execution time
- Exit status

These are returned as structured data via gRPC.


## Failure Cases

- Timeout → process killed and marked as TLE
- Memory overflow → container terminated
- Runtime error → captured and returned
- Internal error → logged and flagged


## Design Decisions

- Separate images per language/version for isolation and reproducibility
- Ephemeral containers to ensure stateless execution
- gVisor for stronger syscall-level isolation