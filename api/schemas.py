""" This file creates the marshmallow Schema to easily convert Todo Objects to JSON
"""
from marshmallow import Schema, fields

class TodoSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    date = fields.DateTime()
