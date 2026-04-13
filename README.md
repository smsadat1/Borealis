# Borealis

A distributed, multi language secure code execution platform using isolated containerized runtimes with strict resource control.


## What it does

 - Executes untrusted code in isolated environments.
 - Supports multiple languages and versions.
 - Enforces strict CPU, memory and time limits
 - Provides real-time execution status streaming
 - Exposes a clean API and CLI


## System overview

Borealis is composed of three core services:

 - APIService -> request handling and orchestration 
 - AuthService -> authentication and API key management
 - RunnerService -> isolated code execution engine

Execution flow: 

  ` Client -> APIService -> AuthService -> RunnerService -> Sandbox (gVisor) `

## Key Capabilites

  - Multi-language execution (Python, C/C++, Go, Java)
  - Versioned runtime support (e.g. Python 3.10 C++17 Go 1.22 )
  - Secure sandboxed execution using gVisor
  - Websocket based execution status streaming
  - Exection history and cancellation support


## Example 

  - Submit code: `POST /execute/`
  - Execution result: `GET /execution/{exec_id}`
  - Cancel execution: `DELETE /execution/{exec_id}`
  - Live updates: `/execute/{exec_id}/stream`

  <!-- add images here   -->


## Design Philosophy

Borealis is designed around isolation, predictability and reproducability when executing untrusted code.

The system prioritizes:
  - strong runtime isolation
  - determinstic execution environments
  - clear separation of concerns across services


## Documentation

Detailed technical documentation is available in `/docs`:

  - Architecture -> `docs/architecture.md`
  - Execution engine -> `docs/runner.md`
  - Security model -> `docs/security.md`
  - API references -> `docs/api.md`
  - Design decisions -> `docs/design-decisions.md`


## Name

Borealis is inspired by the research vessel from *Half Life 2*