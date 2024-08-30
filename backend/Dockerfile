# image for building the app
FROM python:3.12 as build

WORKDIR /app

# install apt dependencies
RUN apt-get update && \
    apt-get install -y make

# install poetry
RUN pip install -U pip poetry==1.7.1

# install dependencies
COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# copy files
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

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--reload", "src.app:app", "--timeout-keep-alive", "120"]

# image for running the app in production
FROM build as prod

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.app:app", "--timeout-keep-alive", "120"]
