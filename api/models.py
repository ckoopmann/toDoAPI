""" This file creates the sqlalchemy model for Todos and ensures that the
table is created in the database
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from yaml import load, Loader
from sqlalchemy import create_engine

DeclBase = declarative_base()

class Todo(DeclBase):
    """ Simple Model with three columns
    """
    __tablename__ = "Todos"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)


# Read db URL from config file and create all necessary tables
# This avoids "table does not exist error" but could probably done more elegantly
with open('config.yml','r') as stream:
    config = load(stream, Loader)
engine = create_engine(config['DB_URIS']['TodoService:Base'])
Todo.metadata.create_all(engine)
