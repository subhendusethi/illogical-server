#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets

logging.basicConfig()

def create_reply(reply_message):
	return json.dumps({ "type" : "text_reply", "message" : reply_message})
async def echo_bot(websocket, path):
	async for message in websocket:
		data = json.loads(message)
		print("data", data)
		if data["action"] == "text_message":
			await asyncio.sleep(0.5)
			await websocket.send(create_reply(data["message"]))

start_server = websockets.serve(echo_bot, "localhost", 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()