from time import sleep
import socketio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from socket_components.message import SocketServerMessageBotChat
import argparse
parser = argparse.ArgumentParser(description='Description of your script')
parser.add_argument('--auth_token', help='Description of the option')

# Parse the command-line arguments
args = parser.parse_args()

# Access the value of the 'option' argument
auth_token_value = args.auth_token

sio = socketio.Client()
sio.connect(f"http://0.0.0.0:8081/?auth={auth_token_value}")

@sio.on('connect')
def on_connect():
    print('Connected to the server!')

@sio.on(SocketServerMessageBotChat.get_event())
def on_custom_event(data: SocketServerMessageBotChat.Data):
    print('Received socketservermessagesbotchat:', data)

@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from the server')

@sio.event
def on_error(data):
    print('Error:', data)

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print('Disconnecting...')
    sio.disconnect()