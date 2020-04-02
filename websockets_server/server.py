#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import sys
import websockets
import os

from models.user import UserSchema

class WebSocketServer:
	def __init__(self, port=5000):
		self.logger = logging.getLogger('websockets')
		self.logger.setLevel(logging.INFO)
		self.logger.addHandler(logging.StreamHandler())
		self.port = port
		self.users_map = {}
		self.users_websocket_map = {}
		self.websockets_users_map = {}

	def __create_reply(self, reply_message, user_alias):
		return json.dumps({ "type" : "text_reply", "message" : reply_message, "alias": user_alias})

	async def __health_check(self, path, request_headers):
		self.logger.info("path incoming ::: {%s}..."%path)
		if path == "/health/":
			return http.HTTPStatus.OK, [], b"OK\n"

	async def __notify_user_taken(self, user_alias, websocket):
		message = "The alias {%s} has been taken"%user_alias
		payload = json.dumps({ "type" : "server_message" , "action_type" : "USER_ALIAS_TAKEN", "message" : message })
		await websocket.send(payload)

	async def __notify_user_count(self, user):
		message = "{%s} joined the chat! The total number of users are now {%d}." % (user.alias, len(self.users_map))
		payload = json.dumps({"type" : "server_message" , "action_type" : "USER_COUNT", "message" : message})
		await asyncio.wait([self.users_websocket_map[user_alias].send(payload) for user_alias in self.users_websocket_map])

	async def __register_user(self, user, websocket):
		print(user)
		if user.alias in self.users_map:
			await self.__notify_user_taken(user.alias, websocket)
			return False
		else:
			self.users_map[user.alias] = websocket
			self.users_websocket_map[user.alias] = websocket
			self.websockets_users_map[websocket] = user.alias
			await self.__notify_user_count(user)
			return True

	async def __unregister_user(self,websocket):
		user_alias = self.websockets_users_map.pop(websocket, None)
		a = self.users_websocket_map.pop(user_alias, None)
		b = self.users_map.pop(user_alias, None)
		await self.__notify_user_count(user)
		return (a and b) != None

	async def __global_chat_server(self, websocket, path):
		try:
			async for message in websocket:
				data = json.loads(message)
				self.logger.info("data incoming ::: {%s}..."%data)
				if data["action"] == "server_registration":
					print("data", data)
					user_schema = UserSchema()
					user = user_schema.load(data["user_data"])
					value = await self.__register_user(user, websocket)
					if not value:
						break
				elif data["action"] == "text_message":
					user_data = data["user_data"]
					await asyncio.wait([self.users_websocket_map[user_alias].send(self.__create_reply(user_data["message"],
						user_data["alias"])) for user_alias in self.users_websocket_map if user_alias != user_data["alias"]])
		finally:
			await self.__unregister_user(websocket)

	def start_server(self):
		self.logger.info('Starting Application Server on port :: {%d}...'%int(self.port))
		start_server = websockets.serve(self.__global_chat_server, '', self.port, process_request=self.__health_check)
		self.logger.info('Starting event loop...')
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()