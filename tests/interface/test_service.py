import json
import pytest
from mock import call
from sqlalchemy import create_engine
from api.models import Todo

valid_test_cases = [('{"name": "English", "date": "2017-01-12 12:00:00"}',
                {"name": "English","id" : 1, "date": "2017-01-12T12:00:00+00:00"}),
                ('{"name": "", "date":"2019-10-12"}',
                {"name": "","id" : 1, "date": "2019-10-12T00:00:00+00:00"})]

invalid_test_cases = [('{"date": "2017-01-12 12:00:00"}'),
                ('{"name": "", "date":"2019-40-12"}')]

def test_can_list_todos(todo_service, web_session, db_session):
    response = web_session.get(url = '/todo/list/')
    print(response.json())
    assert response.status_code == 200

@pytest.mark.parametrize("post_data, get_data", valid_test_cases)
def test_can_add_todo(todo_service, web_session, db_session, post_data, get_data):
    response = web_session.post(url = '/todo/add/', data = post_data)
    assert response.status_code == 201

@pytest.mark.parametrize("post_data", invalid_test_cases)
def test_cant_add_invalidtodo(todo_service, web_session, db_session, post_data):
    response = web_session.post(url = '/todo/add/', data = post_data)
    assert response.status_code == 400

@pytest.mark.parametrize("post_data, get_data", valid_test_cases)
def test_can_get_todo(todo_service, web_session, db_session, post_data, get_data):
    web_session.post(url = '/todo/add/', data = post_data)
    response = web_session.get('/todo/get/1')

    assert response.status_code == 200

    assert response.json() == get_data

@pytest.mark.parametrize("post_data, get_data", valid_test_cases)
def test_can_delete_todo(todo_service, web_session, db_session, post_data, get_data):

    add_response = web_session.post(url = '/todo/add/',data = post_data)
    print(add_response)
    list_response_before = web_session.get('/todo/list/')
    print(list_response_before)
    assert len(list_response_before.json()) == 1

    delete_response = web_session.get('/todo/delete/1')
    assert delete_response.status_code == 200

    list_response_after = web_session.get('/todo/list/')
    assert len(list_response_after.json()) == 0
