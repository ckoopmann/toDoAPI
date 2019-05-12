""" These interface tests check wether the API as a whole behaves as expected on a set of
different test requests posted via HTTP.
"""
import json
import pytest
from mock import call
from sqlalchemy import create_engine
from api.models import Todo

# Valid Test Cases which should be able to be added / retrieved from database
# Each Valid Test Case consists of a combination of json string for POST request and expected response as dictionary
valid_test_cases = [('{"name": "English", "date": "2017-01-12 12:00:00"}',
                {"name": "English","id" : 1, "date": "2017-01-12T12:00:00+00:00"}),
                ('{"name": "", "date":"2019-10-12"}',
                {"name": "","id" : 1, "date": "2019-10-12T00:00:00+00:00"})]

# Invalid JSON strings that should result in response 400 when posted to API
invalid_test_cases = [('{"date": "2017-01-12 12:00:00"}'),
                ('{"name": "", "date":"2019-40-12"}')]

def test_can_list_todos(todo_service, web_session, db_session):
    """ Test wether todos can be listed
    """
    response = web_session.get(url = '/todo/list/')
    print(response.json())
    assert response.status_code == 200

@pytest.mark.parametrize("post_data, get_data", valid_test_cases)
def test_can_add_todo(todo_service, web_session, db_session, post_data, get_data):
    """ Test that each of the valid test cases can be added
    """
    response = web_session.post(url = '/todo/add/', data = post_data)
    assert response.status_code == 201

@pytest.mark.parametrize("post_data", invalid_test_cases)
def test_cant_add_invalidtodo(todo_service, web_session, db_session, post_data):
    """ Test that invalid todos are rejected by API
    """
    response = web_session.post(url = '/todo/add/', data = post_data)
    assert response.status_code == 400

@pytest.mark.parametrize("post_data, get_data", valid_test_cases)
def test_can_get_todo(todo_service, web_session, db_session, post_data, get_data):
    """ Test that all valid test cases can be added and then retrieved from API
    """
    web_session.post(url = '/todo/add/', data = post_data)
    response = web_session.get('/todo/get/1')

    assert response.status_code == 200

    assert response.json() == get_data

@pytest.mark.parametrize("post_data, get_data", valid_test_cases)
def test_can_delete_todo(todo_service, web_session, db_session, post_data, get_data):
    """ Test wether todos can be added and then deleted from database
    """
    add_response = web_session.post(url = '/todo/add/',data = post_data)
    list_response_before = web_session.get('/todo/list/')

    #Ensure that api contains 1 element after adding
    assert len(list_response_before.json()) == 1

    #Delete Element and check response code
    delete_response = web_session.get('/todo/delete/1')
    assert delete_response.status_code == 200

    #Ensure that api contains no elements after deletion
    list_response_after = web_session.get('/todo/list/')
    assert len(list_response_after.json()) == 0
