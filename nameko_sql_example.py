from datetime import datetime
import dateutil.parser
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from app import Todo
from nameko.rpc import rpc
from nameko_sqlalchemy import transaction_retry, Database
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
class TodoService:
    name = "TodoService"

    @rpc
    @transaction_retry()
    def write(self, name, date):
        if(isinstance(date, str)):
            date = dateutil.parser.parse(date)
        obj =Todo(name = name, date = date)
        session = Session()
        session.add(obj)
        session.commit()
        session.close()

    @rpc
    @transaction_retry()
    def get_data(self):
        session = Session()
        results = session.query(Todo).all()
        session.close()
        schema = TodoSchema(many = True)
        return schema.dump(results)

def main():
    service = TodoService()
    service.write('Clean', datetime.now())
    service.write('Cook',"2019-05-04 12:00:00")
    service.write('Homework',"2019-12-31")
    pprint(service.get_data())

if __name__ == '__main__':
    main()
