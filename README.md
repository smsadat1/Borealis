# Borealis

![banner](docs/assets/banner.png)

A multi-language secure code execution platform using isolated containerized runtimes with strict resource control.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Architecture](https://img.shields.io/badge/microservices-enabled-blue)
![Sandbox](https://img.shields.io/badge/isolation-gVisor-red)


## Table of Contents
* [About](#about)
* [Getting Started](#getting-started)
* [Example Usage](#example-usage)
* [Design Philosophy](#design-philosophy)
* [Key Capabilities](#key-capabilities)
* [Non Goals](#non-goals)
* [Documentation](#documentation)
* [Name](#name)


## About

Running untrusted code is not just execution — it is a security problem.

Most systems struggle with:
- unsafe container escape risks
- inconsistent runtime environments
- resource abuse (CPU/memory/time)
- lack of controlled and reliable execution orchestration

Borealis solves this by treating code execution as a hardened infrastructure layer rather than a simple runtime task.


## Getting Started

  - Setup CLI
  ```
  $ git clone git@github.com:smsadat1/Borealis.git 
  $ cd Borealis/borealis
  $ bash build.sh
  ```

  - Setup server (self-host)
  ```
  $ cd Borealis
  $ bash scripts/buildimages.sh
  $ docker compose build --parallel && docker compose up
  ```


## Example Usage

  ![Usage example](docs/assets/example.gif)

  Get API key and login: `$ borealis auth login`

  Send code and testcases to run: `$ borealis runner`



## Design Philosophy

Borealis is designed around isolation, predictability and reproducibility when executing untrusted code.

The system prioritizes:
  - strong runtime isolation
  - deterministic execution environments
  - clear separation of concerns across services


## System overview

Borealis is composed of three core services:

 - APIService -> request handling and orchestration 
 - AuthService -> authentication and API key management
 - RunnerService -> isolated code execution engine

Execution flow: 

  ` Client -> APIService -> AuthService -> RunnerService -> Sandbox (gVisor) `

## Key Capabilities

  - Multi-language execution (Python, C/C++, Go, Java)
  - Versioned runtime support (e.g. Python 3.10 C++17 Go 1.22 )
  - Secure sandboxed execution using gVisor
  - Websocket based execution status streaming
  - Historical records of executions with timestamps



## Non-Goals

To maintain system simplicity and reliability, Borealis intentionally does NOT support:

- multi-file project builds (e.g. full repositories)
- dependency installation (pip, npm, etc.)
- persistent storage between executions
- network access inside execution environments

These constraints ensure predictable, fast, and secure execution.


## Documentation

Detailed technical documentation is available in `/docs`:

  - Architecture -> `docs/architecture.md`
  - Execution engine -> `docs/runner.md`
  - Security model -> `docs/security.md`
  - API references -> `docs/api.md`
  - Design decisions -> `docs/design-decisions.md`


## Name

Borealis is inspired by the research vessel from *Half Life 2*