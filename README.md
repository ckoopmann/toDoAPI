# toDoAPI
Simple nameko api to save todos

This api will enable the client to save and retrieve todos using nameko and nameko-sqlalchemy

## Starting Api

Quickest way to start the service is building and running the docker container

`$ docker build -t todo_api . `

`$ docker run -p 8000:8000 todo_api nameko run --config config.yml api.service`


## Run tests

`$ py.test`
