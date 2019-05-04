import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://christian:password@localhost:5432/todos'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime)
    name = db.Column(db.String(50))

class TodoSchema(ma.ModelSchema):
    class Meta:
        model = Todo

db.create_all()

@app.route('/')
def index():
    todos = Todo.query.all()
    todo_schema = TodoSchema(many=True)
    output = todo_schema.dump(todos).data
    return jsonify({'Todo' : output})

@app.route('/<string:name>')
def add_todo(name):
    now = datetime.datetime.now()
    db.session.add(Todo(Date = now, name = name))
    db.session.commit()
    return jsonify({'Date' : now, 'name' : name})

if __name__ == '__main__':
    app.run(debug=True)
