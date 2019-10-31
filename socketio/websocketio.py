import socketio
import json

from aiohttp import web


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


class Smartmeat():

    def __init__(self, state=None, temperature=None, sticks = []):
        self.state = state
        self.temperature = temperature
        self.sticks = sticks

    
    def __str__(self):
        pass


    def has_data(self):
        return self.state and self.sticks and self.temperature


    def format_msg(self):
        if self.has_data():
            msg = """smartmeat": {
                        "on": {self.state},
                        "temperature": {self.temperature},
                        "stick1": {self.sticks[0]},
                        "stick2": {self.sticks[1]},
                        "stick3": {self.sticks[2]},
                        "stick4": {self.sticks[3]},
                    }""".format(self.state, self.temperature, self.sticks[0], self.sticks[1], self.sticks[2], self.sticks[3])
        print("Formatted message:", msg)

        return msg



async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def message(sid, data):
    print('I received a message!')
    print(data)

@sio.event
def send_data(sid, smartmeat_json):
    print('Sending data!')
    sio.emit(smartmeat_json)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)

# app.router.add_static('/static', 'static')
app.router.add_get('/', index)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
