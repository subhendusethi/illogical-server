#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import sys
import websockets
import os

from models.user_data import UserDataSchema
from models.enums import ClientAction, ServerAction, MessageType


class WebSocketServer:
	def __init__(self, port=5000):
		self.logger = logging.getLogger('websockets')
		self.logger.setLevel(logging.INFO)
		self.logger.addHandler(logging.StreamHandler())
		self.port = port
		self.users_websocket_map = {}
		self.websockets_users_map = {}

	def __create_server_payload(self, payload_type, action, message, alias):
		return json.dumps({
		    "type": payload_type,
		    "action": action,
		    "message": message,
		    "alias": alias
		})

	async def __health_check(self, path, request_headers):
		self.logger.info("path incoming ::: {%s}..." % path)
		if path == "/health/":
			return http.HTTPStatus.OK, [], b"OK\n"

	async def __unregister_user(self, websocket):
		user_alias = self.websockets_users_map.pop(websocket, None)
		a = self.users_websocket_map.pop(user_alias, None)
		await self.__notify_user_count(user_alias)
		return a != None

	async def __notify_user_taken(self, user_alias, websocket):
		message = "The alias {%s} has been taken" % user_alias
		payload = self.__create_server_payload(
		    MessageType.SERVER_MESSAGE.name,
		    ServerAction.USER_ALIAS_TAKEN.name, message, "")
		await websocket.send(payload)

	async def __notify_user_count(self, user_alias):
		message = "{%s} joined the chat! The total number of users are now {%d}." % (
		    user_alias, len(self.users_websocket_map))
		payload = self.__create_server_payload(MessageType.SERVER_MESSAGE.name,
		                                       ServerAction.USER_COUNT.name,
		                                       message, "")
		await asyncio.wait([
		    self.users_websocket_map[registered_user_alias].send(payload)
		    for registered_user_alias in self.users_websocket_map
		])

	def __validate_user(self, user_alias, websocket):
		if websocket in self.websockets_users_map:
			registered_user_alias = self.websockets_users_map[websocket]
			return registered_user_alias == user_alias
		return False

	async def __register_user(self, user_data, websocket):
		if user_data.alias in self.users_websocket_map:
			await self.__notify_user_taken(user_data.alias, websocket)
			return False
		else:
			self.users_websocket_map[user_data.alias] = websocket
			self.websockets_users_map[websocket] = user_data.alias
			self.logger.info("Registered user {%s} onto the global chat..." %
			                 user_data.alias)
			await self.__notify_user_count(user_data.alias)
			return True

	async def __server_registration_consumer(self, user_data, websocket):
		print("here")
		await self.__register_user(user_data, websocket)

	async def __chat_message_broadcast_consumer(self, user_data, websocket):
		provided_user_alias = user_data.alias
		if self.__validate_user(provided_user_alias, websocket):
			print("validated")
			await asyncio.wait([
			    self.users_websocket_map[registered_user_alias].send(
			        self.__create_server_payload(
			            MessageType.SERVER_MESSAGE.name,
			            ClientAction.TEXT_MESSAGE.name, user_data.message,
			            provided_user_alias))
			    for registered_user_alias in self.users_websocket_map
			    if registered_user_alias != provided_user_alias
			])

	async def __global_chat_server(self, websocket, path):
		try:
			async for message in websocket:
				data = json.loads(message)
				self.logger.info("Incoming data to chat server ::: {%s}" %
				                 data)
				user_data_schema = UserDataSchema()
				user_data = user_data_schema.load(data["user_data"])
				if data["action"] == ClientAction.SERVER_REGISTRATION.name:
					await self.__server_registration_consumer(
					    user_data, websocket)
				elif data["action"] == ClientAction.TEXT_MESSAGE.name:
					await self.__chat_message_broadcast_consumer(
					    user_data, websocket)
		finally:
			await self.__unregister_user(websocket)

	def start_server(self):
		self.logger.info('Starting Application Server on port :: {%d}...' %
		                 int(self.port))
		start_server = websockets.serve(self.__global_chat_server,
		                                '',
		                                self.port,
		                                process_request=self.__health_check)
		self.logger.info('Starting event loop...')
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()