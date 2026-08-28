.PHONY: help setup db-up db-down run test test-unit test-integration test-v migrate migrate-down migrate-create migrate-history

help:
	@echo "Available commands:"
	@echo "  setup            - Install dependencies (uv sync)"
	@echo "  db-up            - Start database container (docker-compose)"
	@echo "  db-down          - Stop database container (docker-compose)"
	@echo "  run              - Start the development server (fastapi dev)"
	@echo "  migrate          - Run database migrations (alembic upgrade head)"
	@echo "  migrate-down     - Rollback last migration (alembic downgrade -1)"
	@echo "  migrate-create   - Create migration revision (usage: make migrate-create name=add_users)"
	@echo "  migrate-history  - View migration history (alembic history)"
	@echo "  test             - Run all tests (pytest)"
	@echo "  test-unit        - Run unit tests (pytest tests/unit)"
	@echo "  test-integration - Run integration tests (pytest tests/integration)"
	@echo "  test-v           - Run tests with verbose output (pytest -v)"

setup:
	uv sync

db-up:
	docker-compose -f docker-compose-dev.yaml up -d

db-down:
	docker-compose -f docker-compose-dev.yaml down

run:
	uv run fastapi dev

migrate:
	uv run alembic upgrade head

migrate-down:
	uv run alembic downgrade -1

migrate-create:
	uv run alembic revision --autogenerate $(if $(name),-m "$(name)",)

migrate-history:
	uv run alembic history

test:
	uv run pytest

test-unit:
	uv run pytest tests/unit

test-integration:
	uv run pytest tests/integration

test-v:
	uv run pytest -v
