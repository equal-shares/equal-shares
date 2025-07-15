# image for building the app
FROM python:3.12 as build

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    make \
    libmpfr-dev \
    libmpc-dev \
    libgmp-dev

# install poetry
RUN pip install -U pip poetry==1.7.1

# Configure poetry and pip for better reliability
RUN poetry config virtualenvs.create false && \
    poetry config installer.max-workers 4 && \
    pip config set global.timeout 1000

# install dependencies in multiple steps to avoid timeouts
COPY pyproject.toml poetry.lock /app/

# First install larger packages separately
RUN pip install pandas matplotlib numpy

# Then use poetry for the rest with retries
RUN poetry install --no-root || \
    poetry install --no-root || \
    poetry install --no-root

# copy files
# Copy Makefile so we can invoke it inside the container
COPY Makefile /app/Makefile
# Copy flake8 config
COPY .flake8 /app/.flake8

# Copy source and tests
COPY src /app/src
COPY tests /app/tests

# install the project as a package
RUN poetry install

# image for linting the app
FROM build as lint

COPY . /app/

ENTRYPOINT ["make", "lint"]

# image for testing the app
FROM build as test

WORKDIR /app

COPY . /app/

ENTRYPOINT ["make", "test"]

# image for running the at development
FROM build as dev

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--reload", "src.app:app", "--timeout-keep-alive", "600"]

# image for running the app in production
FROM build as prod

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.app:app", "--timeout-keep-alive", "600"]
