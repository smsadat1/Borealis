# Security Model

This system is designed to safely execute untrusted user-submitted code.

The primary goal is to prevent:
- host system compromise
- container escape
- resource exhaustion
- unauthorized data access

Security is enforced through multiple layers including isolation, resource control, and restricted execution environments.


## Threat Model

The system assumes that all submitted code is potentially malicious.

Possible attack vectors include:
- attempts to escape the container environment
- excessive resource consumption (CPU, memory, infinite loops)
- attempts to access the network or external systems
- privilege escalation within the container
- exploitation of runtime vulnerabilities


## Isolation Strategy

Code execution occurs inside containers using gVisor (runsc).

gVisor provides an additional isolation layer by intercepting system calls in user space, reducing the attack surface compared to standard container runtimes.

Each execution:
- runs in a separate container
- uses a minimal runtime image
- is destroyed after execution completes


## Container Restrictions

Execution environments are configured with strict security constraints:

- No network access
- No privileged mode
- No new privileges (no_new_privs)
- Read-only filesystem (where applicable)
- Limited system capabilities


## Resource Limits

To prevent denial-of-service attacks:

- CPU usage is restricted per execution
- Memory usage is capped
- Execution timeouts are enforced
- Long-running or stuck processes are terminated


## Execution Lifecycle

1. Code is submitted via API
2. RunnerService selects appropriate runtime image
3. A container is launched using gVisor
4. Resource limits and restrictions are applied
5. Code is executed
6. Output is captured
7. Container is destroyed


## Runtime Considerations

Different languages and runtimes introduce different risk profiles.

To mitigate this:
- Each language/version is isolated in its own container image
- Only required dependencies are included
- Runtime environments are kept minimal


## Limitations

- Security depends on correctness of underlying container runtime and gVisor
- Zero-day vulnerabilities in runtimes may still pose risks
- Side-channel attacks are not fully mitigated
- No persistent storage isolation is currently enforced