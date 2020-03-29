#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def create_reply(reply_message):
	return json.dumps({ "type" : "text_reply", "message" : reply_message})

async def health_check(path, request_headers):
	logger.info("path incoming ::: {%s}..."%path)
	if path == "/health/":
		return http.HTTPStatus.OK, [], b"OK\n"

async def echo_bot(websocket, path):
	async for message in websocket:
		data = json.loads(message)
		logger.info("data incoming ::: {%s}..."%data)
		if data["action"] == "text_message":
			await asyncio.sleep(0.5)
			await websocket.send(create_reply(data["message"]))

logger.info('Starting Application Server...')
start_server = websockets.serve(echo_bot, 'localhost', 6789, process_request=health_check)
logger.info('Starting event loop...')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()