# taskapi

Small api for running tasks in the background

## Pre-requisite

1. redis server

## Setup

1. Install `pyenv` ([link](https://github.com/pyenv/pyenv))
   - at the time of writing, app as tested using Python 3.8.3
2. `python -m venv .venv`
3. `source .venv/bin/acrivate`
4. `python -m pip install --upgrade pip && python -m pip install -r requirements.txt`

## Sample .env file

```env
REDIS_HOST=localhost
REDIS_PORT=6379
ALLOWED_COMMANDS=/usr/bin/dd,true,false
```

*ALLOWED_COMMANDS* is a comma separated list of commands that can be executed in your environment

## How To run and test

1. Create .env file
2. Run redis-server in the background
3. Run the app `flask run`
4. Run the worker `python manage.py workers`
5. Use your favorite API client to send requests

## Example API calls using httpie

```bash
$ python -m httpie --pretty=all http://localhost:8000/task/ binary=/usr/bin/dd options:='["if=/dev/urandom","of=/tmp/test.img","bs=1024","count=5M"]'
HTTP/1.0 201 CREATED
Content-Length: 51
Content-Type: application/json
Date: Wed, 24 Jun 2020 01:01:13 GMT
Server: Werkzeug/1.0.1 Python/3.8.3

{
    "id": "8b99c19f-b869-4ccc-857e-a81cb55864ca"
}

$ python -m httpie --pretty=all http://localhost:8000/task/8b99c19f-b869-4ccc-857e-a81cb55864ca
HTTP/1.0 200 OK
Content-Length: 76
Content-Type: application/json
Date: Wed, 24 Jun 2020 01:01:37 GMT
Server: Werkzeug/1.0.1 Python/3.8.3

{
    "id": "8b99c19f-b869-4ccc-857e-a81cb55864ca",
    "status": "finished"
}
```

