# toDoAPI
Simple nameko api to save todos

This api will enable the client to save and retrieve todos using nameko and nameko-sqlalchemy

## Starting API

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

## Query API
This api accepts requests to add, retrieve and delete a single ToDo Task as well as lis all entries currently stored.
###Add Todo
To Add a todo one submits a post request with the name and date of the task as json data:

```sh
$ curl -XPOST -d '{"name": "English", "date": "2017-01-12 12:00:00"}' 'http://localhost:8000/todo/add/'
```

On sucessfull creation of the todo the api response with status code 200 and the data as it was entered into the database including autoincremented id column and parsed date column:

```sh
{"name": "English", "id": 9, "date": "2017-01-12T12:00:00+00:00"}
```


## Run tests
To run the tests first install the requirements:

`$ pip install --no-cache-dir -r requirements.txt `

And then run from the top level of this repository:

`$ py.test`
