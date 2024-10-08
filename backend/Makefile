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
	python -m isort .

black:
	 python -m black .

# Run the formatters for the backend
fix: isort black

flake8:
	python -m flake8 .

black-check:
	 python -m black --check --diff .

mypy:
	python -m mypy .

# Run the linters for the backend
lint: flake8 black-check mypy

# Run the formatters and linters for the backend
fix-lint: fix lint

# Run the tests for the backend
test:
	poetry run python -m doctest src/algorithm/**.py
	poetry run pytest

# Run the load test
test-locust:
	poetry run locust --host https://api.arielcs.xyz

# Run examples
run-algorithm:
	poetry run python -m src run-algorithm ./input_for_algorithm.json

examples-run-algorithm:
	python examples/algorithm.py
