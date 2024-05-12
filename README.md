# equal-shares

## Table of content

* [About](#about)
* [Technologies](#technologies)
  * [Versions](#versions)
* [Files Structure](#files-structure)
  * [Production Files Structure](#production-files-structure)
* [Environment Variables](#environment-variables)
  * [Backend](#backend)
  * [Frontend](#frontend)
* [Requirements](#requirements)
  * [For Using Locally](#for-using-locally)
  * [For Development](#for-development)
* [Installation - Local](#installation---local)
  * [For Development](#for-development)
* [Usage](#usage)
  * [Management](#management)
* [Development](#Development)
* [Production](#production)
  * [Production Scripts](#production-scripts)
  * [Production Requirements](#production-requirements)
  * [Production Installation](#production-installation)
* [Links](#links)
* [Authors](#authors)
* [License](#license)

## About

## Technologies

* python - As programming language for the backend
* conda - For managing python environment
* poetry - For managing python dependencies
* FastAPI - As framework for the backend
* uvicorn - For running the backend usinn ASGI
* gunicorn - For running the backend in production
* PostgresSQL - As database
* docker - For development in production of the backend
* docker compose - For local development
* React - As framework for the frontend
* TypeScript - As programming language for the frontend
* Vite - As build tool for the frontend
* Tailwind CSS - For styling the frontend
* MUI - As UI library for the frontend

### Versions

* python 3.12
* node 21
* poetry 1.7.1
* PostgresSQL 16

## Files Structure

* backend - The backend API
  * src
    * routers
      * admin - routes for managmenet
      * form - routes for the frontend
      * report - routes for the reports of the votes and the algorithm
    * app.py - the entry of the backend application
    * config.py - contains the configuration of the backend. uses environment variables
    * database.py - database connection
    * exceptions.py - custom exceptions
    * models.py - database models and queries
    * schemas.py - schemas of the API
    * security.py - security functions
  * Dockerfile - for building the backend locally
  * equal-shares-api-private-key.pem - private RSA key for the API
  * equal-shares-api-public-key.pem - public RSA key for the API
  * gunicorn_conf.py - configuration for gunicorn
  * Makefile - commands for development
  * pyproject.toml - configuration and poetry dependencies
* frontend - The frontend application
  * public - static files
  * src
    * components
    * api.ts - for using the backend API
    * App.tsx - the main component
    * index.tsx - the entry of the frontend application
    * schema.ts - schemas of the API
  * Dockerfile - for building the frontend locally
  * package.json - dependencies and commands for development
* prod - files that copied to the production server
  * nginx
    * equal_shares - configuration for nginx
  * backend.env - environment variables for the backend service, will copy to /app/backend.env
  * equal_shares.service - config for backend service
  * frontend.env - environment variables for build the frontend, will copy to /app/frontend.env
* res - resources
* scripts - scripts for production
  * config-gunicorn.sh - for update configuring of gunicorn service
  * config-nginx.sh - for update configuring of nginx service
  * pull.sh - for pulling the latest version of the code, build the application and restart the services
  * restart.sh - for restarting the services
* docker-compose.yml - for local development
* environment.yml - conda environment
* LICENSE - MIT license
* Makefile - commands for development
* README.md - this file

### Production Files Structure

* /app - the root directory of the project
  * /backend.env - environment variables for the backend service
  * /equal-shares - the project directory
  * /frontend.env - environment variables for build the frontend
  * /keys
    * equal-shares-api-private-key.pem - private RSA key for the API
    * equal-shares-api-public-key.pem - public RSA key for the API
  * gunicorn.sock - socket for gunicorn
  * static - static files for the frontend application
  * access_log - log file for the access of the API
  * error_log - log file for the errors of the API

## Environment Variables

### Backend

Table of the required environment variables for the backend:

| Variable            | Description                       |
|---------------------|-----------------------------------|
| PG_DATABASE         | PostgresSQL database name         |
| PG_USER             | PostgresSQL user                  |
| PG_PASSWORD         | PostgresSQL password              |
| PG_HOST             | PostgresSQL host                  |
| ADMIN_KEY           | uuid for admin key                |
| API_RSA_PUBLIC_KEY  | path to public RSA key for API    |
| API_RSA_PRIVATE_KEY | path to private RSA key for API   |

Table of the optional environment variables for the backend:

| Variable | Description      | Default |
|----------|------------------|---------|
| PG_PORT  | PostgresSQL port | 5432    |


### Frontend

Table of the required environment variables for the frontend:

| Variable      | Description      |
|---------------|------------------|
| VITE_API_HOST | API backend host |

## Requirements

### For Using Locally

* docker

### For Development

* conda
* node 21.5.0

## Installation - Local

Create or Copy the RSA keys of the API to the backend directory.
* ./backend/equal-shares-api-private-key.pem
* ./backend/equal-shares-api-public-key.pem

Run the following commands to install:

```bash
git clone git@github.com:omer-priel/equal-shares.git
cd equal-shares

docker compose build
```

### For Development

Run the following commands to install for development:

```bash
conda env create -f environment.yml
conda activate equal-shares

cd backend
poetry install

cd ../frontend
npm ci
```

## Usage

For running the frontend, backend and the database run the following command:

```bash
docker compose up
```

The API will run on http://localhost:8000/

In the API Dashbord (Swagger UI) you can see, manage and test the System. \
admin_key is key for authentication as admin and you can have it from docker-compose.yml under the environments of backend.

And the frontend will run on http://localhost:5173/

The frontend is a simple form for voting. \
For authentication the URL needs the paramters email and token.

For example: http://localhost:5173/?email=some.mail%40example.com&token=jJfGlbWO7%2BxiPCaMofLnX2zYFIGZOuBQ1Vg65zAyUd0EVAfk36y%2FIzH67UAUGsrjlvMKMsF9%2FIAlMC66Ner2g9vyP%2F%2FazBMirFpN9spDyFeHAiEk3tmz%2FlCXnQfz%2BDmayKZsxO5n%2BLf1bs4eF8TR6u8wwQumV%2BnErXvF1%2BCy4W0%3D

You can create a token using /admin/create-token in the API Dashbord.

### Management

Creating the database tables: \
In the API Dashbord run /admin/create-tables

Change settings: \
In the API Dashbord run /admin/set-settings \
* max_total_points - the maximum total points a voter can give to all the projects in total
* points_step - a number that points in votes can be divided by.
  For example if `points_step` is 100, vouter cannot give 150 points to a project but can give 100 or 200 points.

Delete all the projects, votes and vouters: \
In the API Dashbord run /admin/delete-projects-and-votes

Delete votes and voters: \
In the API Dashbord run /admin/delete-votes

Add new projects from XLSX file: \
In the API Dashbord run /admin/add-projects \
* xlsx_file - the XLSX file with the projects. The columns should be:
  column 1: name of the project
  column 2: min points of the project
  column 3: max points of the project
  column 4: this column is not in use
  column 5: description of the project,

Get the Projects and Settings as JSON format: \
In the API Dashbord run /admin/projects

## Development

For clean, safe and maintainable deployment exits number of Linters and Formatters. \
* Formaters - are tools that automatically format and fix the code.
  * Backend: isort, black
  * Frontend: Prettier, ESLint
* Linters - are tools for check the code.
 * Backend: flake8, black, mypy
 * Frontend: ESLint

Before running the formatter and linters, make sure conda environment is activated and node version is 21.5.0 \
For running the formatters and linters run the following commands:

```bash
make fix-lint
```

For running only the formatters run the following commands:

```bash
make fix
```

For running only the linters run the following commands:

```bash
make lint
```

## Production

On the production server already installed Python 11, Poetry, Node 21.5.0 and PostgresSQL. \
For managing the server you have scripts under /app/scripts

The project will be saved in: /app/equal-shares

### Production Scripts

This following scripts will: \
* pull the latest version of the code from GitHub
* update the dependencies of backend
* update the dependencies of frontend
* build the frontend
* restart the API (gunicorn) service and nginx service

```bash
bash ./scripts/pull.sh
```

For restarting the services run the following command:

```bash
bash ./scripts/restart.sh
```

For deleting the database run the following command:

```bash
psql -U postgres -c "DROP DATABASE equal_shares;"
```

For configuring the nginx run the following command:

```bash
bash ./scripts/config-nginx.sh
```

For configuring the gunicorn run the following command:

```bash
bash ./scripts/config-gunicorn.sh
```

### Production Requirements

* Linux
* Python 3.12 - Required before installation
* Poetry
* NodeJS
* PostgresSQL

### Production Installation

In the next steps we will show how to install the project on new production server.

1. Use SSH for connecting to the server
2. Run the following commands for update server:

```bash
sudo apt update
sudo apt upgrade -y
```

3. For installing the requirements for backend run the following commands:

```bash
sudo apt install pipx -y
pipx ensurepath
pipx install poetry==1.7.1
```

4. Exit the SSH and connect again for activating the poetry

For checking the installation of python and poetry run the following commands:

```bash
python3 -V
poetry --version
```

Python should be 3.12 and poetry should be 1.7.1

5. For installing the requirements for frontend run the following commands:

```bash
curl -sL https://deb.nodesource.com/setup_21.x | sudo -E bash -
sudo apt-get install -y nodejs
```

For checking the installation of NodeJS and npm run the following commands:

```bash
node -v
npm -v
```

Node should be 21.5.0 or higher version of 21 \
And npm should be 10.5.0 or higher

6. For installing PostgresSQL run the following commands:

```bash
apt install -y libpq-dev
apt install -y postgresql-16
apt install -y postgresql-client-16
apt install -y postgresql-doc-16
apt install -y postgresql-server-dev-16
```

7. Exit the SSH and connect again for activating the PostgresSQL

For checking the installation of PostgresSQL run the following commands:

```bash
psql -V
```

PostgresSQL should be 16

For checking the PostgresSQL run the following commands:

```bash
sudo -u postgres psql -c "\l"
```

It will show the table of the databases, that contains the default database `postgres`

8. For installing Nginx, Uvicorn and Gunicorn run the following commands:

```bash
sudo apt install -y nginx
sudo apt install -y gunicorn
sudo apt install -y uvicorn
```

Run the following commands for checking the installation of Nginx:

```bash
nginx -v
sudo ufw app list
```

It will show you under Available applications the `Nginx Full`, `Nginx HTTP`, `Nginx HTTPS` and `OpenSSH` \

Now run the following commands for configuring the firewall:

```bash
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw allow 8000
sudo ufw enable
```

For checking the status of the firewall run the following command:

```bash
sudo ufw status
```

9. In Web Browser (like Google Chrome) enter the IP of the server and you should see the Nginx welcome page
10. exit the SSH and connect again

11. For installing the project run the following commands:

```bash
mkdir /app
cd /app
git clone https://github.com/equal-shares/equal-shares.git
cd equal-shares
```

12. For installing the backend run the following commands:

```bash
cd /app/equal-shares/backend
poetry install
```

13. For installing the frontend run the following commands:

```bash
cd /app/equal-shares/frontend
npm ci
```

14. Create a non-root user for running the services:

```bash
sudo adduser --disabled-password --gecos GECOS equal-shares
```

For checking the user run the following command:

```bash
id equal-shares
```

15. For configuring the environment variables run the following commands:

```bash
cp /app/equal-shares/prod/backend.env /app/backend.env
cp /app/equal-shares/prod/frontend.env /app/frontend.env
```

For creating Admin Key run the following command:

```bash
python3 -c "import uuid;print(uuid.uuid4())"
```

Save the output of the command, this is the Admin Key for managing the API \
Copy the output and paste it to the /app/backend.env as value of ADMIN_KEY using nano:
  
```bash
nano /app/backend.env
```

Use nano for editing VITE_API_HOST in /app/frontend.env \
Replace the value of VITE_API_HOST with `http://<server-ip>:8000` the `server-ip` is the IP of the server

```bash
nano /app/frontend.env
```

15. Run the folowing commands for create directory for the Keys:
  
```bash
mkdir /app/keys
```

16. For adding the api RSA keys disconnect the SSH \
    Copy the RSA keys of the API to production server using the following commands:

Note: replace <server-ip> with the IP of the server and you should have the keys in your current directory

```bash
scp equal-shares-api-private-key.pem root@<server-ip>:/app/keys/equal-shares-api-private-key.pem
scp equal-shares-api-public-key.pem root@<server-ip>:/app/keys/equal-shares-api-public-key.pem
```

17. For config the Nginx and Gunicorn, connect to the serverv and run the following commands:

```bash
bash /app/equal-shares/scripts/config-nginx.sh
bash /app/equal-shares/scripts/config-gunicorn.sh
```

18. For build and start the services run the following commands:

```bash
bash /app/equal-shares/scripts/pull.sh
```

## Links

* [ca website](https://faircourse.csariel.xyz/)
* [ca-frontend](https://github.com/ariel-research/cap-frontend)
  Original frontend - React
* [ca-backend](https://github.com/ariel-research/cap-backend)
  Original backend - Django
* [equalshares.net](https://equalshares.net/)
* [Final-Project](https://github.com/ElhaiMansbach/Final-Project)
  For the algorithm of equal shares - Flask and React

# Authors

* Bar Nahmias
* Didi Avidad
* Omer Priel

## License

MIT
