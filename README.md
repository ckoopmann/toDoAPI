# toDoAPI
Simple nameko api to save todos

This api will enable the client to save and retrieve todos using nameko and nameko-sqlalchemy

## Starting Api

### Using Docker
The quickest and easiest way to start the service is building and running the docker container:

`$ docker build -t todo_api . `

`$ docker run -p 8000:8000 todo_api nameko run --config config.yml api.service`

This assumes that you have docker installed and the docker daemon running normally and you have navigated to the top level of this repository.

### Without Docker
Alternatively the app can be run from the command line by first installing the required python packages (including nameko) with:

`$ pip install --no-cache-dir -r requirements.txt `

And then running

`$ nameko run --config config.yml api.service`

This assumes that you have Python 3.7+ and Pip installed and have navigated to the top level of this repository.

## Run tests
To run the tests first install the requirements:

`$ pip install --no-cache-dir -r requirements.txt `

And then run from the top level of this repository:

`$ py.test`
