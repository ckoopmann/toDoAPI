from marshmallow import Schema, fields

class TodoSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    date = fields.DateTime()
