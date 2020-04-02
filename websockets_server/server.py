#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import sys
import websockets
import os

class WebSocketServer:
	def __init__(self, port=5000):
		self.logger = logging.getLogger('websockets')
		self.logger.setLevel(logging.INFO)
		self.logger.addHandler(logging.StreamHandler())
		self.port = port

	def __create_reply(self, reply_message):
		return json.dumps({ "type" : "text_reply", "message" : reply_message})

	async def __health_check(self, path, request_headers):
		self.logger.info("path incoming ::: {%s}..."%path)
		if path == "/health/":
			return http.HTTPStatus.OK, [], b"OK\n"

	async def __echo_bot(self, websocket, path):
		async for message in websocket:
			data = json.loads(message)
			self.logger.info("data incoming ::: {%s}..."%data)
			if data["action"] == "text_message":
				await asyncio.sleep(0.5)
				await websocket.send(self.__create_reply(data["message"]))

	def start_server(self):
		self.logger.info('Starting Application Server on port :: {%d}...'%int(self.port))
		start_server = websockets.serve(self.__echo_bot, '', self.port, process_request=self.__health_check)
		self.logger.info('Starting event loop...')
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()