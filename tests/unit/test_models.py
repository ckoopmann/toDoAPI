""" These unit tests check wether the Database behaves as expected regarding
the functionality necessary for the API
"""
from api.models import Todo
from dateutil.parser import parse

def test_can_create_todo(db_session, todo):
    """ Test wether a todo can be added to the database
    """
    db_session.add(todo)
    db_session.commit()
    assert todo.id > 0



def test_can_get_todo(db_session, todo):
    """ Test wether a todo can be added to and retrieved from the db
    """
    db_session.add(todo)
    db_session.commit()
    obj = db_session.query(Todo).filter(Todo.id == todo.id).first()
    assert obj.id == todo.id

def test_can_delete_todo(db_session, todo):
    """ Test wether a todo can be added to and deleted from the db
    """
    db_session.add(todo)
    db_session.commit()
    num_deleted = db_session.query(Todo).filter(Todo.id == todo.id).delete()
    assert num_deleted == 1
    db_session.commit()
    num_left = db_session.query(Todo).filter(Todo.id == todo.id).count()
    assert num_left == 0

def test_can_list_todos(db_session):
    """ Test wether a whole list of todos can be added to db and correctly
    retrieved by getting all entries from databse
    """
    todo_list = [Todo(name = 'Cleaning', date = parse('2019-04-23 12:00:00')),
    Todo(name = 'Homework', date = parse('2019-04-23 14:00:00'))]

    db_session.add_all(todo_list)
    db_session.commit()
    results = db_session.query(Todo).all()

    assert len(results) == len(todo_list)

    for i in range(len(results)):
        assert results[i] == todo_list[i]
