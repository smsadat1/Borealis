# Borealis

Borealis is a secure, multi-language online code execution system built with **Starlette**.  
It allows users to submit code in **C, C++, and Python**, run it in isolated sandboxed environments, and receive **real-time output** via WebSockets.  
Inspired by Half-Life 2’s mysterious research labs, Borealis combines safe execution, live streaming, and a clean REST API for modern coding experimentation.

---

## Features

- Run C, C++, and Python code safely
- Restrict standard libraries and disable internet access
- Real-time output streaming via WebSocket
- Job history and status management
- Async and scalable with Starlette

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/executions` | Submit new code execution job |
| GET    | `/executions` | Get history of executions |
| GET    | `/executions/{id}` | Get execution result |
| DELETE | `/executions/{id}` | Cancel execution |
| WS     | `/executions/{id}/stream` | Stream real-time stdout/stderr |

---

## Example Request

**Submit a Python job:**

```bash
curl -X POST http://localhost:8000/executions \
  -H "Content-Type: application/json" \
  -d '{
        "language": "python",
        "source_code": "print(\"Hello, Borealis!\")",
        "stdin": ""
      }'