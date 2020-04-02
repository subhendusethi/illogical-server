import datetime as dt

from marshmallow import Schema, fields


class User():
  def __init__(self, name, alias, websocket):
    self.name = name
    self.alias = alias
    self.created_at = dt.datetime.now()
    
  def __repr__(self):
    return '<User(name={self.name!r})>'.format(self=self)


class UserSchema(Schema):
  name = fields.Str()
  alias = fields.Number()
  created_at = fields.Date()

  @post_load
  def make_user(self, data, **kwargs):
      return User(**data)