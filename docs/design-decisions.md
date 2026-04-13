# Design Decisions

The system prioritizes isolation, predictability and performance when executing untrusted code.

## Framework selection per service

### APIService - Starlette

The API layer is intentionally kept minimal to prioritize reliability in the execution pipeline.
 - Starlette provides a lightweight ASGI foundation with strong async support.
 - Avoids unnecessary abstraction overload.
 - Enables efficient handling of concurrent execution request.
 - Native support for WebSockets allows future real-time execution updates.
This keeps the API laeyr focused on request orchestration rather than business complexity. 

### AuthService - FastAPI

Authentication requires stricter input validation and structured request handling.
 - FastAPI provides built-in validation via type hints.
 - Reduces boilerplate for request parsing and schema enforcement.
 - Maintains performance while improving correctness.
This keeps the API laeyr focused on request orchestration rather than business complexity. 

## Interservice communication

### gRPC-based communication
All services communicate using gRPC instead of REST.
 - Binary protocol reduces overhead compared to JSON.
 - Strong typing via protobuf enforces contract correctness.
 - Better suited for internal service-to-service communications.
 - Not designed for human interaction -> optimized for machine performance.
This ensures high-performance, reliable internal communication.

## Execution environment design

### Dedicated runtime images per language/version

Instead of monolithic execution image, the system uses images per language and version.
 - Avoids unnecessary dependencies in execution environments.
 - Reduces image size and startup overhead.
 - Imrpoves reproducibility across executions.
 - Enables fine-grained control over runtime behavior.
This design favors predictability and isolation over convenience.


## Sandbox and isolation strategy 

### gVisor-based execution (runsc)
Execution is sandboxed using gVisor instead of standard Docker runtime approaches like DinD (Docker-in-Docker) or DooD (Docker outside of Docker).
 - Intercepts syscalls in user space for stronger isolation
 - Reduces risk of container escape attacks
 - Lightweight compared to full virtualization
 - Suitable for running untrusted code safely
This provides a defense-in-depth approach to sandboxing.


## Security constraints
Execution environments enforce strict limitations:
 - CPU and memory limits to prevent resource abuse
 - Execution timeouts to avoid infinite loops
 - No network access to prevent data exfiltration
 - No privilege escalation to maintain isolation boundaries
These constraints ensure the system remains secure under adversarial workloads.