import json
import pytest
from mock import call
from sqlalchemy import create_engine
from api.models import Todo


def test_can_list_todos(todo_service, web_session, db_session):
    response = web_session.get('/todo/list/')
    print(response.json())
    assert response.status_code == 200

def test_can_add_todo(todo_service, web_session, db_session):
    response = web_session.post('/todo/add/?name=English&date=2019-12-01')
    assert response.status_code == 200

def test_can_get_todo(todo_service, web_session, db_session):
    web_session.post('/todo/add/?name=English&date=2019-12-01')
    response = web_session.get('/todo/get/1')

    assert response.status_code == 200

    assert response.json() == {'date': '2019-12-01T00:00:00+00:00',
                                'id': 1,
                                'name': 'English'}

def test_can_delete_todo(todo_service, web_session, db_session):
    web_session.post('/todo/add/?name=English&date=2019-12-01')

    list_response_before = web_session.get('/todo/list/')
    assert len(list_response_before.json()) == 1

    delete_response = web_session.get('/todo/delete/1')
    assert delete_response.status_code == 200

    list_response_after = web_session.get('/todo/list/')
    assert len(list_response_after.json()) == 0
