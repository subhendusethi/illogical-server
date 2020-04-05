import datetime as dt
from marshmallow import Schema, fields, post_load

class UserData():
	def __init__(self, alias, message):
		self.alias = alias
		self.message = message
		self.created_at = dt.datetime.now()
	def __repr__(self):
		return '<UserData(name={self.alias!r},message={self.message!r})>'.format(self=self)

class UserDataSchema(Schema):
	alias = fields.Str()
	message = fields.Str()
	created_at = fields.Date()

	@post_load
	def make_user(self, data, **kwargs):
		return UserData(**data)