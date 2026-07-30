# Sifr

A production-ready FastAPI service showcasing modern DevOps practices, including containerization, CI/CD automation, structured logging, automated testing, and a clean, scalable project structure.

---

## Overview

**Sifr** is a lightweight backend service designed to demonstrate production-oriented DevOps workflows and software engineering best practices. It serves as a practical reference for building, testing, containerizing, and validating Python applications using modern DevOps tooling.

---

## Architecture

```text
Browser / curl
      │
      ▼
 FastAPI (app/main.py)
      │
      ├── GET  /health        ← Liveness probe
      ├── GET  /ready         ← Readiness probe
      ├── GET  /items/        ← List all items
      ├── POST /items/        ← Create item
      ├── GET  /items/{id}    ← Get single item
      ├── PUT  /items/{id}    ← Update item
      └── DELETE /items/{id}  ← Delete item

In production, replace the in-memory store with PostgreSQL, MySQL, or Redis.
```

### Design Highlights

- **FastAPI** for building high-performance APIs
- **Pydantic v2** for request and response validation
- **Structured logging** using Python's `logging` module
- **Multi-stage Docker builds** for smaller, secure runtime images
- **Non-root container execution** for improved security
- **Docker Compose** for streamlined local development
- **GitHub Actions** for continuous integration
- **Automated testing** with coverage reporting

---

## Project Structure

```text
sifr/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── item.py
│   └── routes/
│       ├── __init__.py
│       ├── health.py
│       └── items.py
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   └── test_items.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── .dockerignore
```

---

## Running Locally

### Option A — Python

```bash
cd sifr

python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements-dev.txt

cp .env.example .env

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# or

make install-dev
make run
```

Open:

```
http://localhost:8000/docs
```

---

### Option B — Docker

```bash
docker build --target runtime -t sifr:local .

docker run -d \
  --name sifr \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  sifr:local

curl http://localhost:8000/health
```

---

### Option C — Docker Compose

```bash
docker-compose up --build -d

docker-compose logs -f

docker-compose down
```

---

## Running Tests

```bash
pytest tests/ --cov=app --cov-report=term-missing -v

# or

make test
```

---

## CI/CD Pipeline

Sifr uses GitHub Actions to automatically validate every change pushed to the repository.

```text
Push to GitHub
      │
      ▼
GitHub Actions
      │
      ├── Lint
      │      ruff check
      │      ruff format --check
      │
      ├── Test
      │      pytest
      │      Coverage report
      │
      └── Build
             Docker image
             Smoke test (/health)
```

The pipeline ensures code quality, automated tests, and container builds succeed before changes are merged or released.

---

## DevOps Features

| Feature | Implementation |
|----------|----------------|
| **Containerization** | Multi-stage Docker build with a non-root runtime image |
| **Continuous Integration** | GitHub Actions pipeline for linting, testing, and building |
| **Testing** | Pytest with coverage reporting |
| **Observability** | Structured logging with `/health` and `/ready` endpoints |
| **Configuration** | Environment variables managed via Pydantic Settings |
| **Security** | Non-root Docker runtime and environment-based configuration |
| **Developer Experience** | Makefile shortcuts and Docker Compose for local development |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `Sifr` | Application name |
| `APP_VERSION` | `1.0.0` | Application version |
| `ENVIRONMENT` | `development` | Runtime environment |
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Bind port |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |

Copy `.env.example` to `.env` and adjust the values for your environment.

---

## Roadmap

- PostgreSQL integration
- Redis caching
- JWT authentication and authorization
- OpenAPI authentication
- Automated deployment via GitHub Actions
- Kubernetes manifests
- Helm chart
- Prometheus metrics
- Grafana dashboards
- Terraform infrastructure provisioning

---

## License

This project is licensed under the MIT License.

---

> **Sifr** is a production-oriented FastAPI project that demonstrates modern DevOps workflows, clean architecture, containerization, testing, and continuous integration practices.