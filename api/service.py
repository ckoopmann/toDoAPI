from datetime import datetime
import dateutil.parser
from nameko.rpc import rpc
from nameko.web.handlers import http
from nameko_sqlalchemy import transaction_retry, Database
from api.models import Todo, DeclBase
from api.schemas import TodoSchema
import json


class TodoService:
    """
    Service class that is instantiated by nameko to run the todo api
    """
    name = "TodoService"



    db = Database(DeclBase)



    @http('POST','/todo/add/')
    @transaction_retry()
    def add(self, request):
        """
        Method for adding a new todo to the database via POST request

        Example request ::

            {
                "name": "EnglishLesson",
                "date": "2017-01-12 12:00:00"
             }


        The response contains the posted data with the parsed date and an added id column ::

            {
                "id" : 1,
                "name": "EnglishLesson",
                "date": "2017-01-12T12:00:00+00:00"
            }
        """

        dict = json.loads(request.get_data(as_text = True))

        try:
            #Get the name and date values from request. This might raise KeyError
            name = dict['name']
            date = dict['date']

            #If date value is a string try converting to datetime. This might raise Value Error
            if(isinstance(date, str)):
                date = dateutil.parser.parse(date)

            #Create SQL Alchemy Todo Object and add new entry to the database
            obj =Todo(name = name, date = date)
            schema = TodoSchema()
            session = self.db.get_session()
            session.add(obj)
            session.commit()

            #Prepare response data using marshmallow schema
            response = json.dumps(schema.dump(obj).data)
            session.close()
            return 201, response

        # Handle errors resulting from incomplete or invalid data in the request and return corresponding response code
        except (ValueError, KeyError):
            return 400, 'Bad Request'



    @http('GET','/todo/delete/<int:id>')
    @transaction_retry()
    def delete(self, request, id):
        """
        Method for deleting a single todo referenced by the id

        Example request ::

            /todo/delete/1


        The response contains data which was deleted from the database ::

            {
                "id" : 1,
                "name": "EnglishLesson",
                "date": "2017-01-12T12:00:00+00:00"
            }
        """
        schema = TodoSchema()
        session = self.db.get_session()

        #Get data for response
        obj = session.query(Todo).filter(Todo.id == id).first()
        response = json.dumps(schema.dump(obj).data)

        #Delete entry from DB
        session.query(Todo).filter(Todo.id == id).delete()
        session.commit()
        session.close()
        return response


    @http('GET','/todo/get/<int:id>')
    @transaction_retry()
    def get(self, request, id):
        """
        Method retrieving a single todo referenced with its id

        Example request ::

            /todo/get/1


        The response contains data which was deleted from the database ::

            {
                "id" : 1,
                "name": "EnglishLesson",
                "date": "2017-01-12T12:00:00+00:00"
            }

        """
        session = self.db.get_session()
        results = session.query(Todo).filter(Todo.id == id).first()
        session.close()
        schema = TodoSchema()
        return json.dumps(schema.dump(results).data)


    @http('GET','/todo/list/')
    @transaction_retry()
    def list(self, request):
        """
        Returns list of all todos in the database

        Example request ::

            /todo/list


        The response contains all todos that are saved in the database::

            [
                {
                    "id" : 1,
                    "name": "EnglishLesson",
                    "date": "2017-01-12T12:00:00+00:00"
                },
                {
                    "id" : 2,
                    "name": "FrenchLesson",
                    "date": "2017-01-13T13:00:00+00:00"
                }
            ]

        """
        session = self.db.get_session()
        results = session.query(Todo).all()
        session.close()
        schema = TodoSchema(many = True)
        return json.dumps(schema.dump(results).data)
