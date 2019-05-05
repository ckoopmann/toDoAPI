import json
import pytest
from mock import call
from sqlalchemy import create_engine
from api.models import Todo

@pytest.fixture()
def db_create_table(db_url):
        engine = create_engine(db_url)
        Todo.metadata.create_all(engine)


def test_can_list_todos(todo_service, web_session, db_session):
    response = web_session.get('/todo/list/')
    assert response.status_code == 200

def test_can_add_todo(todo_service, web_session, db_session):
    response = web_session.post('/todo/add/?name=English&date=2019-12-01')
    assert response.status_code == 200
