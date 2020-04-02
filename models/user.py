import datetime as dt
from marshmallow import Schema, fields, post_load


class User():
  def __init__(self, name, alias):
    self.name = name
    self.alias = alias
    self.created_at = dt.datetime.now()
  def __repr__(self):
    return '<User(name={self.name!r},alias={self.alias!r})>'.format(self=self)


class UserSchema(Schema):
  name = fields.Str()
  alias = fields.Str()
  created_at = fields.Date()
  @post_load
  def make_user(self, data, **kwargs):
      return User(**data)