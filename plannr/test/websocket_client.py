from time import sleep
import socketio

sio = socketio.Client()
sio.connect("http://127.0.0.1:8081/")

@sio.on('connect')
def on_connect():
    print('Connected to the server!')

@sio.on('schedule_generated')
def on_custom_event(data):
    print('Received custom event:', data)

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