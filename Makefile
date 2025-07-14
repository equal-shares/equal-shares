SHELL:=/usr/bin/env bash

.PHONY: test-dev serve logs fix lint fix-lint test docker-test clean

clean:
	make -C backend clean

# Run the linters of both the backend and frontend
fix:
	make -C backend fix
	cd frontend && npm run prettier:fix
	cd frontend && npm run eslint:fix

# Run the formatters of both the backend and frontend
lint:
	make -C backend lint
	cd frontend && npm run eslint:lint

# Run the formatters and linters
fix-lint: fix lint

# Run the tests of the backend
test:
	make -C backend test

# Run tests in Docker containers
docker-test:
	docker compose -f test.docker-compose.yaml up --build

# Run tests in running dev containers
test-dev:
	docker exec -it equal-shares-backend-1 python -m pytest

# Run the examples
examples-run-algorithm:
	make -C backend examples-run-algorithm

# development
serve:
	docker compose -f dev.docker-compose.yaml up --build -d

# View live logs from all dev containers
logs:
	docker compose -f dev.docker-compose.yaml logs -f

ssh-to-prod:
	ssh root@arielcs.xyz
