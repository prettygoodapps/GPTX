.PHONY: help install dev-install lint test security docs validate-all clean format type-check stop cleanup deploy-railway
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	poetry install --only=main

dev-install: ## Install all dependencies including development
	poetry install
	poetry run pre-commit install

format: ## Format code with black and isort
	poetry run black src/ tests/ scripts/
	poetry run isort src/ tests/ scripts/

type-check: ## Run type checking with mypy
	poetry run mypy src/

lint: ## Run all linting tools
	@echo "Running black..."
	poetry run black --check src/ tests/ scripts/
	@echo "Running isort..."
	poetry run isort --check-only src/ tests/ scripts/
	@echo "Running flake8..."
	poetry run flake8 src/ tests/ scripts/
	@echo "Running mypy..."
	poetry run mypy src/
	@echo "✅ All linting checks passed!"

test: ## Execute test suite with coverage
	poetry run pytest --cov=src/gptx --cov-report=term-missing --cov-report=html --cov-fail-under=80

security: ## Security vulnerability scan
	poetry run bandit -r src/ -f json -o bandit-report.json
	poetry run bandit -r src/
	@echo "✅ Security scan completed!"

docs: ## Generate and validate documentation
	@echo "Generating documentation..."
	poetry run sphinx-build -b html docs/ docs/_build/html
	@echo "Validating docstring coverage..."
	poetry run python scripts/check_docstrings.py
	@echo "✅ Documentation generated and validated!"

validate-all: ## Run complete validation suite
	@echo "🔍 Running complete Kilo Code validation suite..."
	@echo ""
	@echo "1. Code formatting and linting..."
	$(MAKE) lint
	@echo ""
	@echo "2. Type checking..."
	$(MAKE) type-check
	@echo ""
	@echo "3. Security scanning..."
	$(MAKE) security
	@echo ""
	@echo "4. Test suite with coverage..."
	$(MAKE) test
	@echo ""
	@echo "5. Documentation validation..."
	$(MAKE) docs
	@echo ""
	@echo "🎉 All validation checks passed! Project is Kilo Code compliant."

clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf bandit-report.json
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run: ## Run the application
	poetry run python src/gptx/main.py

dev: ## Run the application in development mode
	poetry run uvicorn gptx.main:app --reload --host 0.0.0.0 --port 8000

stop: ## Stop development server and clean up processes
	@echo "🛑 Stopping development server..."
	@pkill -f "python scripts/dev_server.py" || true
	@pkill -f "uvicorn gptx.main:app" || true
	@pkill -f "port 8005" || true
	@pkill -f "port 8000" || true
	@echo "✅ Development server stopped!"

cleanup: stop clean ## Stop server and clean up all artifacts
	@echo "🧹 Complete cleanup finished!"

deploy-railway: ## Deploy to Railway platform
	@echo "🚀 Deploying GPTX Exchange to Railway..."
	./scripts/deploy_railway.sh

build: ## Build the package
	poetry build

publish: ## Publish to PyPI (requires authentication)
	poetry publish

pre-commit: ## Run pre-commit hooks on all files
	poetry run pre-commit run --all-files

setup: ## Initial project setup
	@echo "🚀 Setting up GPTX Exchange for development..."
	$(MAKE) dev-install
	@echo "✅ Setup complete! Run 'make validate-all' to verify everything works."