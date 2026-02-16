# Uvicorn Integration Guide

## Overview

**Uvicorn** is an ASGI web server that can be integrated with Python Click CLI projects for development server functionality, mock API services, or documentation serving.

This guide explains how to use uvicorn with the generated Python CLI client.

## When to Use Uvicorn

### Recommended Use Cases

1. **Development Server** - Test CLI against local mock API
2. **Documentation Server** - Serve auto-generated or markdown documentation
3. **Admin Dashboard** - Web UI for configuration management
4. **Health Checks** - Expose monitoring endpoints
5. **Telemetry/Metrics** - Serve Prometheus-style metrics
6. **Mock API** - Create test fixtures during development

### Not Recommended For

- ✗ Production API serving (use production-grade servers)
- ✗ High-traffic applications
- ✗ Complex WebSocket applications
- ✗ Heavy CPU-bound operations

## Installation

### Basic Installation

```bash
pip install uvicorn
```

### With Optional Dependencies

```bash
# With uvloop (faster)
pip install uvicorn[standard]

# With all features
pip install uvicorn[all]
```

### Verify Installation

```bash
uvicorn --version
# Uvicorn version 0.24.0
```

## Basic Usage

### Hello World Example

Create `app.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}
```

Run the server:

```bash
uvicorn app:app --reload
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

Test the server:

```bash
curl http://localhost:8000/
# {"message":"Hello World"}

curl http://localhost:8000/health
# {"status":"ok"}
```

## Configuration

### Command-Line Options

**Common Options:**

```bash
uvicorn app:app                    # Basic startup
--host 0.0.0.0                    # Bind to all interfaces
--port 8000                        # Port number (default: 8000)
--reload                          # Auto-reload on code changes
--workers 4                        # Number of worker processes
--log-level info                  # Log level (critical, error, warning, info, debug)
--no-access-log                   # Disable access logging
--env-file .env                   # Load environment variables
```

**Full Command Example:**

```bash
uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --log-level debug \
  --access-log
```

### Configuration File (uvicorn.ini)

Create `uvicorn.ini`:

```ini
[server]
host = 0.0.0.0
port = 8000
workers = 4
reload = true
log-level = info
access_log = true

[ssl]
ssl_version = 17
ssl_cert_reqs = 0
ssl_ca_certs = null
ssl_ciphers = null
```

Run with config file:

```bash
uvicorn app:app --config uvicorn.ini
```

### YAML Configuration

Create `uvicorn.yaml`:

```yaml
host: 0.0.0.0
port: 8000
workers: 4
reload: true
log_level: info
access_log: true
```

## Integration with Click CLI

### Project Structure

```
my-api-client/
├── Makefile
├── uvicorn.ini
├── src/
│   └── my_cli/
│       ├── __init__.py
│       ├── cli.py              # Click CLI entry point
│       ├── client.py           # API client
│       └── server.py           # Uvicorn/FastAPI app (optional)
└── tests/
```

### Example: Mock API Server

Create `src/my_cli/server.py`:

```python
"""Optional development server for testing."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Mock API")

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/api/users")
async def list_users():
    """Mock users endpoint."""
    return {
        "users": [
            {"id": "1", "name": "Alice"},
            {"id": "2", "name": "Bob"}
        ]
    }

@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """Mock user detail endpoint."""
    return {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }

@app.post("/api/users")
async def create_user(name: str, email: str):
    """Mock create user endpoint."""
    return {
        "id": "new",
        "name": name,
        "email": email,
        "created": True
    }
```

### Makefile Integration

Add to `Makefile`:

```makefile
.PHONY: serve serve-prod serve-debug

serve:
	@echo "Starting development server..."
	uvicorn src.my_cli.server:app --reload --port 8000

serve-prod:
	@echo "Starting production server..."
	uvicorn src.my_cli.server:app --host 0.0.0.0 --port 8000 --workers 4

serve-debug:
	@echo "Starting debug server..."
	uvicorn src.my_cli.server:app --reload --port 8000 --log-level debug

serve-docs:
	@echo "Starting documentation server..."
	python -m http.server 8001 --directory docs
```

### Usage

```bash
# Development mode (with auto-reload)
make serve

# Production mode (multiple workers)
make serve-prod

# Debug mode (verbose logging)
make serve-debug

# In another terminal, test the server
curl http://localhost:8000/api/users
```

## Advanced Usage

### Custom Middleware

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Logging Configuration

```python
import logging
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### Environment Variables

Create `.env`:

```
APP_NAME=My API
APP_ENV=development
DEBUG=true
DATABASE_URL=sqlite:///./test.db
```

Load in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()

app_name = os.getenv("APP_NAME", "Default App")
debug = os.getenv("DEBUG") == "true"
```

## Troubleshooting

### Port Already in Use

**Problem:** `Address already in use`

**Solutions:**

```bash
# Use different port
uvicorn app:app --port 8001

# Kill process using port 8000
lsof -i :8000
kill -9 <PID>

# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module Not Found

**Problem:** `ModuleNotFoundError: No module named 'app'`

**Solutions:**

```bash
# Make sure you're in the correct directory
cd /path/to/project

# Install package in development mode
pip install -e .

# Use proper path
uvicorn src.my_cli.server:app
```

### Changes Not Reloading

**Problem:** Code changes aren't being picked up

**Solutions:**

```bash
# Make sure --reload is enabled
uvicorn app:app --reload

# Check file permissions
chmod -R 644 src/

# Restart server
```

### Connection Refused

**Problem:** `Connection refused` when accessing http://localhost:8000

**Solutions:**

```bash
# Make sure server is running
ps aux | grep uvicorn

# Check if port is listening
netstat -tuln | grep 8000

# Try explicit address
curl http://127.0.0.1:8000

# Check firewall
```

## Performance Tuning

### Worker Processes

```bash
# Single process (development)
uvicorn app:app

# Multiple workers (production)
uvicorn app:app --workers 4

# Recommended: (CPU cores * 2) + 1
# 4 cores = 9 workers
uvicorn app:app --workers 9
```

### Buffer Sizes

```bash
# Increase buffer for large requests
uvicorn app:app --interface=asgi3 --no-server-header
```

### Connection Pooling

```python
# In your app.py
from sqlalchemy.pool import NullPool

engine = create_engine(
    "postgresql://user:password@localhost/db",
    poolclass=NullPool
)
```

## Deployment Considerations

### Development

```bash
# Quick start with reload
make serve
```

### Staging

```bash
# Multiple workers, no reload
make serve-prod

# Or directly:
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production

Use a reverse proxy (Nginx, Apache):

```nginx
upstream uvicorn {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://uvicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Or use process manager (Supervisor, systemd):

```ini
[program:my-api]
command = /usr/bin/python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
directory = /var/www/my-api
user = www-data
autostart = true
autorestart = true
stderr_logfile = /var/log/my-api/err.log
stdout_logfile = /var/log/my-api/out.log
```

## Monitoring

### Health Checks

```python
@app.get("/health")
async def health():
    return {"status": "ok"}

# Monitor with:
curl http://localhost:8000/health
```

### Metrics Endpoint

```python
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

request_count = Counter('requests_total', 'Total requests')

@app.middleware("http")
async def track_requests(request: Request, call_next):
    request_count.inc()
    return await call_next(request)

# Serve metrics at /metrics
metrics_app = make_wsgi_app()
```

### Logging

```bash
# Check logs in real-time
uvicorn app:app --log-level debug | grep -E "GET|POST|ERROR"

# Save to file
uvicorn app:app > server.log 2>&1 &

# View logs
tail -f server.log
```

## References

- [Uvicorn Documentation](https://www.uvicorn.org/)
- [ASGI Specification](https://asgi.readthedocs.io/)
- [FastAPI with Uvicorn](https://fastapi.tiangolo.com/deployment/concepts/)

## Summary

Uvicorn provides a lightweight, fast development server for testing Python CLI projects:

✓ Use for development and testing
✓ Configure via command-line or config files
✓ Integrate with Makefile for easy startup
✓ Add custom middleware and routes as needed
✓ Monitor with health checks and logging

For production, use a proper reverse proxy and process manager.
