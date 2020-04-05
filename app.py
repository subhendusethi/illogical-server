import os
import logging

from websockets_server.server import WebSocketServer

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

PORT = None
try:
	PORT = os.environ['PORT']
except Exception as e:
	logger.error("Got exception while finding environment port")
	raise Exception("Unable to detect the PORT mapping")

if __name__ == '__main__':
	web_socket_server = WebSocketServer(PORT)
	web_socket_server.start_server()