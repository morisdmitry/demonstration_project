# Demonstration project

CRUD operations with user data by phone number
working using FastAPI and MongoDB

## Features

- Created CRUD operations
- async working using FastAPI
- async connection to MongoDB
- async connection to RedisDB
- field validation in create handler
- cached query in get handler
- creates index by `phone_number` field

#### handlers

- create or update (number is unique field)
- get by phone (include request to DaData service for gets country code by current country)
- delete by phone

## How to run?

For the applicaiton to work properly you need Docker(or install data bases locally) and python 3.8 or higher

1. check free ports in docker-compose.yaml
2. .env file contains sensitive data for connect to DaData service (now it's actual data but who knows what happend later. You can change it on yours)
3. run `docker-compose up -d`
4. application working inside docker local network that created when docker-compose is running

## How to test?

Tests runs locally

1. check free ports in docker-compose-local.yaml
2. run `docker compose -f docker-compose-local.yaml up -d`
3. .env file contains RUN_TESTS. Set flag as True to switch databases (check ports in .env file and docker-compose-local.yaml file)
4. run `pytest tests` in root directory
