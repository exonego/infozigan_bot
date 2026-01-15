# Default goal
.DEFAULT_GOAL := help

# Variables
# Usage: make mig m="migration_message"
m = "Migration"

.PHONY: help stub mig run-docker

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

stub:  ## Generate Fluentogram stubs
	@echo "Generating stubs..."
	python -X utf8 -m fluentogram -d ./I18N/locales/ru/LC_MESSAGES/ -o ./I18N/locales/stub.pyi
	@echo "Done!"

mig:  ## Create a new alembic migration. Usage: make mig m="message"
	@echo "Creating migration: $(m)"
	alembic revision --autogenerate -m "$(m)"

up: ## Rebuild and start docker containers
	docker compose up --build

down: ## Stop docker containers
	docker compose down
