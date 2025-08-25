# Makefile for rehash 🌀
# Run `make help` to see available commands.

.PHONY: help install dev clean \
        parse-all parse-fitness parse-out parse-out-fitness \
        test lint coverage

help: ## Show this help menu
	@echo "Available commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

# -------------------------
# 📦 Installation & Dev
# -------------------------

install: ## Install rehash into current environment
	pip install .

dev: ## Install rehash in editable (dev) mode with test deps
	pip install -e ".[dev]"

clean: ## Remove build/test/coverage caches
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +

# -------------------------
# 🧪 Testing & QA
# -------------------------

test: ## Run pytest test suite
	pytest -v

lint: ## Run ruff + mypy for linting & type checking
	ruff check src/rehash
	mypy src/rehash

coverage: ## Run pytest with coverage report
	pytest --cov=rehash --cov-report=term --cov-report=html

version: ## Show the current rehash version
	@python -c "import rehash; print(rehash.__version__)"

# -------------------------
# 🌀 CLI Examples
# -------------------------

parse-all: ## Parse ALL conversations (rehash parse-export export.zip --out out.json)
	rehash parse-export export.zip --out out.json

parse-fitness: ## Parse ONLY fitness conversations (rehash parse-export export.zip --out out.json --fitness-only)
	rehash parse-export export.zip --out out.json --fitness-only

parse-out: ## Parse custom export: make parse-out ZIP=my.zip OUT=outdir
	rehash parse-export $(ZIP) --out $(OUT)

parse-out-fitness: ## Parse custom export (fitness-only): make parse-out-fitness ZIP=my.zip OUT=outdir
	rehash parse-export $(ZIP) --out $(OUT) --fitness-only
