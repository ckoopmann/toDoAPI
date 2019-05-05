from datetime import datetime
import dateutil.parser
from app import Todo
from nameko.rpc import rpc
from nameko_sqlalchemy import transaction_retry, Database
from models import Todo, DeclBase
from schemas import TodoSchema

class TodoService:
    name = "TodoService"

    db = Database(DeclBase)

    @rpc
    @transaction_retry()
    def add(self, name, date):
        if(isinstance(date, str)):
            date = dateutil.parser.parse(date)
        obj =Todo(name = name, date = date)
        session = self.db.get_session()
        session.add(obj)
        session.commit()
        session.close()

    @rpc
    @transaction_retry()
    def delete(self, id):
        session = self.db.get_session()
        session.query(Todo).filter(Todo.id == id).delete()
        session.commit()
        session.close()


    @rpc
    @transaction_retry()
    def get(self, id):
        session = self.db.get_session()
        results = session.query(Todo).filter(Todo.id == id).first()
        session.close()
        schema = TodoSchema()
        return schema.dump(results).data


    @rpc
    @transaction_retry()
    def list(self):
        session = self.db.get_session()
        results = session.query(Todo).all()
        session.close()
        schema = TodoSchema(many = True)
        return schema.dump(results).data
