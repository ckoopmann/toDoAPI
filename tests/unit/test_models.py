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

def test_can_delete_todo(db_session, todo):
    db_session.add(todo)
    db_session.commit()
    num_deleted = db_session.query(Todo).filter(Todo.id == todo.id).delete()
    assert num_deleted == 1
    db_session.commit()
    num_left = db_session.query(Todo).filter(Todo.id == todo.id).count()
    assert num_left == 0
