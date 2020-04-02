from websockets_server.server import WebSocketServer
import os

PORT = None
try:
	PORT = os.environ['PORT']
except Exception as e:
	logger.error("Got exception while getting environ port")
	raise Exception("Unable to detect the PORT mapping")

if __name__ == '__main__':
	web_socket_server = WebSocketServer(PORT)
	web_socket_server.start_server()
	app.run(host='0.0.0.0', port=PORT)