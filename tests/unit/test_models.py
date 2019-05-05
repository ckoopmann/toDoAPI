from api.models import Todo

def test_can_create_todo(db_session, todo):
    db_session.add(todo)
    db_session.commit()
    assert todo.id > 0



def test_can_get_todo(db_session, todo):
    db_session.add(todo)
    db_session.commit()
    obj = db_session.query(Todo).filter(Todo.id == todo.id).first()
    assert obj.id == todo.id
