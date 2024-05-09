SHELL:=/usr/bin/env bash -O globstar

# Clean the backend from cache
clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

isort:
	python -m isort src

black:
	 python -m black src

# Run the formatters for the backend
fix: isort black

flake8:
	python -m flake8 src

black-check:
	 python -m black --check --diff src

mypy:
	python -m mypy src

# Run the linters for the backend
lint: flake8 black-check mypy

# Run the formatters and linters for the backend
fix-lint: fix lint
