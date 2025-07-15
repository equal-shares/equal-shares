SHELL:=/usr/bin/env bash

# Find all python files under src/algorithm for doctest target
PY_ALGO_FILES:=$(shell find src/algorithm -name '*.py')

# Clean the backend from cache
clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

isort:
	python -m isort .

black:
	 python -m black .

# Run the formatters for the backend
fix: isort black

flake8:
	python -m flake8 --config .flake8 .

black-check:
	 python -m black --check --diff .

mypy:
	python -m mypy .

# Run the linters for the backend
lint: flake8

# Run the formatters and linters for the backend
fix-lint: fix lint

# Run the tests for the backend
test:
	poetry run python -m doctest $(PY_ALGO_FILES)
	poetry run pytest

# Run the load test
test-locust:
	poetry run locust --host https://api.arielcs.xyz

# Run the algorithm
run-algorithm:
	poetry run python -m src run-algorithm input_for_algorithm.json

run-algorithm-with-result:
	poetry run python -m src run-algorithm input_for_algorithm.json results.json

# Run the examples
examples-run-algorithm:
	python examples/algorithm.py
