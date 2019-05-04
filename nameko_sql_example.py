import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from app import Todo
from nameko_sqlalchemy import transaction_retry
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import Schema, fields, pprint


DeclBase = declarative_base(name='examplebase')

class Todo(DeclBase):
    __tablename__ = "Todos"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)


class TodoSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    date = fields.DateTime()


engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine)


Todo.metadata.create_all(engine)

@transaction_retry()
def write(name, date):
    obj =Todo(name = name, date = date)
    session = Session()
    session.add(obj)
    session.commit()
    session.close()

@transaction_retry()
def get_data():
    session = Session()
    results = session.query(Todo).all()
    session.close()
    schema = TodoSchema(many = True)
    return schema.dump(results)


write('Clean', datetime.datetime.now())

pprint(get_data())
