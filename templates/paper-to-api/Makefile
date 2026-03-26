.PHONY: serve docker deploy bench test clean

# ============================================================
# paper-to-api — Makefile
# One command for everything. No excuses.
# ============================================================

APP_NAME ?= my-model-api
PORT ?= 8000
WORKERS ?= 1

# --- Development ---
serve:
	@echo "Starting dev server at http://localhost:$(PORT)"
	@echo "API docs at http://localhost:$(PORT)/docs"
	uvicorn app.main:app --host 0.0.0.0 --port $(PORT) --reload

# --- Docker ---
docker:
	docker build -t $(APP_NAME):latest .

deploy:
	docker compose up -d
	@echo ""
	@echo "API running at http://localhost:$(PORT)"
	@echo "API docs at http://localhost:$(PORT)/docs"

stop:
	docker compose down

# --- Testing ---
test:
	pytest tests/ -v

bench:
	@echo "Running load test — 50 users, 60 seconds"
	python scripts/bench.py --users 50 --duration 60 --host http://localhost:$(PORT)

health:
	python scripts/health_check.py http://localhost:$(PORT)

# --- Utilities ---
clean:
	docker compose down -v 2>/dev/null || true
	docker rmi $(APP_NAME):latest 2>/dev/null || true
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

logs:
	docker compose logs -f --tail=100
