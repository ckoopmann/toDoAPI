from datetime import datetime
import dateutil.parser
from nameko.rpc import rpc
from nameko.web.handlers import http
from nameko_sqlalchemy import transaction_retry, Database
from api.models import Todo, DeclBase
from api.schemas import TodoSchema
import json


class TodoService:
    name = "TodoService"



    db = Database(DeclBase)



    @http('POST','/todo/add/')
    @transaction_retry()
    def add(self, request):
        name = request.args.get('name')
        date = request.args.get('date')
        if(isinstance(date, str)):
            date = dateutil.parser.parse(date)
        obj =Todo(name = name, date = date)
        schema = TodoSchema()
        session = self.db.get_session()
        session.add(obj)
        session.commit()
        response = json.dumps(schema.dump(obj).data)
        session.close()
        return response


    @http('GET','/todo/delete/<int:id>')
    @transaction_retry()
    def delete(self, request, id):
        schema = TodoSchema()
        session = self.db.get_session()
        obj = session.query(Todo).filter(Todo.id == id).first()
        response = json.dumps(schema.dump(obj).data)
        session.query(Todo).filter(Todo.id == id).delete()
        session.commit()
        session.close()
        return response


    @http('GET','/todo/get/<int:id>')
    @transaction_retry()
    def get(self, request, id):
        session = self.db.get_session()
        results = session.query(Todo).filter(Todo.id == id).first()
        session.close()
        schema = TodoSchema()
        return json.dumps(schema.dump(results).data)


    @http('GET','/todo/list/')
    @transaction_retry()
    def list(self, request):
        session = self.db.get_session()
        results = session.query(Todo).all()
        session.close()
        schema = TodoSchema(many = True)
        return json.dumps(schema.dump(results).data)
