
# Politico Backend

[![Build Status](https://travis-ci.com/deemukeni/politico_backend.svg?branch=develop)](https://travis-ci.com/deemukeni/politico_backend)
[![Maintainability](https://api.codeclimate.com/v1/badges/57f88fbf525a980973f7/maintainability)](https://codeclimate.com/github/deemukeni/politico_backend/maintainability)


Politico enables citizens give their mandate to politicians running for different government offices
while building trust in the process through transparency.

The repo for the frontend is available at https://github.com/deemukeni/politico_backend


API Documentation https://documenter.getpostman.com/view/6135035/RznLGw8a

Project API demo is hosted on Heroku

## Prerequisites

- VS Code
- Python 3.6
- Postman

## Installation

- Clone the repo
```
$ git clone
```

- CD into the folder
```
$ cd politico_backend
```

- Create a virtual environment
```
$ python3 -m venv env
```

- Activate the virtual environment
```
$ source env/bin/activate
```

- Install dependencies
```
$ pip install -r requirements.txt
```

- Set the environment variables
```
$ source .env_sample
```

- Run the app
```
$ python run.py or flask run
```

- Testing
```
$ pytest --cov=app
```
## API Endpoints (V1)

| **HTTP METHOD** |	**URI** |	**ACTION**
| --- | --- | --- |
| **POST** | `/api/v1/parties` | create party |
| **GET** |	`/api/v1/parties` | Get all parties |
| **GET** |	`/api/v1/parties/<int:id>` | Get party by id |
| **PATCH** |	`/api/v1/parties/<int:id>`	| Edit party |
| **DELETE** |	`/api/v1/parties/<int:id>`	| Delete a party |
| **POST** |	`/api/v1/offices`	| create office |
| **GET** |	`/api/v1/offices`	| Get all offices |
| **GET** |	`/api/v1/offices/<int:id>`	| Get office by id |
| **PATCH** |	`/api/v1/offices/<int:id>`	| Edit office |
| **DELETE** |	`/api/v1/offices/<int:id>`	| Delete a office |

## Author

Deborah Mukeni - [Dee](https://github.com/deemukeni)


