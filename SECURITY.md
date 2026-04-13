# Security Policy

Borealis is designed to safely execute untrusted code using strong isolation and resource constraints.

## Reporting a Vulnerability

If you discover a security issue, please report it responsibly by contacting:

<smsadat788@gmail.com>

Please avoid publicly disclosing vulnerabilities until they have been addressed.

## Security Model

Borealis enforces multiple layers of security including:

- container-based isolation using gVisor
- strict CPU, memory, and execution limits
- no network access in execution environments
- ephemeral execution containers

For detailed technical information, see:
`docs/security.md`