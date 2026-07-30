.PHONY: install install-dev run test lint format build up down logs clean help

PYTHON  = python3
PIP     = pip
IMAGE   = Sifr
TAG     = local

help:
	@echo ""
	@echo "  install       Install runtime dependencies"
	@echo "  install-dev   Install dev + test dependencies"
	@echo "  run           Run the API locally (uvicorn)"
	@echo "  test          Run tests with coverage"
	@echo "  lint          Lint with Ruff"
	@echo "  format        Auto-format with Ruff"
	@echo "  build         Build the Docker image"
	@echo "  up            Start services with docker-compose"
	@echo "  down          Stop docker-compose services"
	@echo "  logs          Tail docker-compose logs"
	@echo "  clean         Remove caches and artifacts"
	@echo ""

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80 -v

lint:
	ruff check app/ tests/

format:
	ruff format app/ tests/

build:
	docker build --target runtime -t $(IMAGE):$(TAG) .

up:
	docker-compose up --build -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage coverage.xml htmlcov
