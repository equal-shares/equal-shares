SHELL:=/usr/bin/env bash -O globstar

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

docker-test:
	docker compose -f test.docker-compose.yaml up --build

# Run the examples
examples-run-algorithm:
	make -C backend examples-run-algorithm

# development
serv:
	docker compose -f dev.docker-compose.yaml up --build

ssh-to-prod:
	ssh root@arielcs.xyz
