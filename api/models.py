from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from yaml import load, Loader
from sqlalchemy import create_engine

DeclBase = declarative_base()

class Todo(DeclBase):
    __tablename__ = "Todos"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)


with open('config.yml','r') as stream:
    config = load(stream, Loader)

engine = create_engine(config['DB_URIS']['TodoService:Base'])
Todo.metadata.create_all(engine)
