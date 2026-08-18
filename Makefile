.PHONY: help setup db-up db-down run

help:
	@echo "Available commands:"
	@echo "  setup    - Install dependencies (uv sync)"
	@echo "  db-up    - Start database container (docker-compose)"
	@echo "  db-down  - Stop database container (docker-compose)"
	@echo "  run      - Start the development server (fastapi dev)"

setup:
	uv sync

db-up:
	docker-compose -f docker-compose-dev.yaml up -d

db-down:
	docker-compose -f docker-compose-dev.yaml down

run:
	uv run fastapi dev
