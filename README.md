# equal-shares

## Technologies

* python - As programming language for the backend
* conda - For managing python environment
* poetry - For managing python dependencies
* FastAPI - As framework for the backend
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
* res - resources
* scripts - scripts for production
  * config-nginx.sh - for configuring nginx
  * config-uvicorn.sh - for configuring uvicorn
  * pull.sh - for pulling the latest version of the code, build the application and restart the services
  * restart.sh - for restarting the services
* docker-compose.yml - for local development
* environment.yml - conda environment
* LICENSE - MIT license
* Makefile - commands for development
* README.md - this file

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

## Installation

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

## Production

On the production server already installed Python 11, Poetry, Node 21.5.0 and PostgresSQL. \
For managing the server you have scripts under /app/scripts

The project will be saved in: /app/equal-shares

### Production Requirements

* Linux - Required before installation
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

8. For installing Nginx run the following commands:

```bash
sudo apt install -y nginx
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

### Production Scripts

This following scripts will: \
* pull the latest version of the code from GitHub
* update the dependencies of backend
* update the dependencies of frontend
* build the frontend
* restart the uvicorn and nginx services

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

For configuring the uvicorn run the following command:

```bash
bash ./scripts/config-uvicorn.sh
```

## Deployment

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
