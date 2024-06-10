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
	python -m isort src tests

black:
	 python -m black .

# Run the formatters for the backend
fix: isort black

flake8:
	python -m flake8 src tests

black-check:
	 python -m black --check --diff .

mypy:
	python -m mypy src tests

# Run the linters for the backend
lint: flake8 black-check mypy

# Run the tests for the backend
doctest:
	python -m doctest src/algorithm/computation.py
	python -m doctest src/algorithm/equal_shares.py
	python -m doctest src/algorithm/utils.py

pytest:
	python -m pytest -k tests

test: doctest pytest

# Run the formatters and linters for the backend
fix-lint: fix lint
