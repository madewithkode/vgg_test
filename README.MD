# VGG Interview Test

This repository houses the code for the VGG Interview scheduling App - A Django application for interview scheduling that applies the CRUD functionalities, the system should have two accounts, one for the interviewer and one for candidate.

## Retrieve code

-   `$ git clone git@gitlab.com:safetity/safetity-backend.git`

## Requrements

This project requires the following system dependencies:


*   Python 3.9

*   PostgreSQL

*   RabbitMQ

*   Virtualenv(Recommended)

## Setup

#### Database

Create a PostgresSQL database following the configurations on `src/vgg_interview/settings/dev.py`

`$ sudo -u postgres psql`

`postgres=# create database <database_name>;`

`postgres=# create user <user_name> with encrypted password '<password>';`

`postgres=# grant all privileges on database <database_name> to <user_name>;`

#### Environment Variables

This project requires a `.env` file with the following variables, please create one in the project's root folder and supply the relevant credentials.

*   DEBUG
*   SECRET_KEY
*   DATABASE_HOST
*   DATABASE_NAME
*   DATABASE_USERNAME
*   DATABASE_PASSWORD
*   BROKER_URL

## Running


-   `$ virtualenv -p /usr/bin/python3.9 virtualenv`  - While in the project root, run this to create a virtual environment named virtualenv
-   `$ pip install requirements.txt` - While in the project root, run this to install all external packages required to run project.
-   Cd into `src` folder and run `$ python manage.py migrate` This applies the project's migration(if any)
-   While still in `src` folder, run `$ python manage.py runserver` This should now start the django app at the default localhost:8000
-   run `celery -A vgg_interview.settings.celery.CELERY beat -l info` in a new terminal inside `src` folder to start celery beat for periodic tasks.

