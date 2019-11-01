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
        # Sticks follow this pattern:
        # self.sticks = [
        #                   {
        #                       "stick1": True,
        #                       "time_active": "00:00"
        #                   },
        #                   {
        #                       "stick2": True,
        #                       "time_active": "00:00"
        #                   },
        #                   {
        #                       "stick3": True,
        #                       "time_active": "00:00"
        #                   },
        #                   {
        #                       "stick4": True,
        #                       "time_active": "00:00"
        #                   },
        #               ]

    
    def __str__(self):
        return self.format_msg()


    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


    def has_data(self):
        if not self.state:
            return False
        if not self.temperature:
            return False
        if not self.sticks:
            return False
        return True


    def format_msg(self):
        formatted_msg = {}
        if self.has_data():
            msg = self.serialize()
            formatted_msg["smartmeat"] = msg
        else:
            print("WARN: At least one attribute of SmartMeat is None")

        print("Formatted message:", formatted_msg)

        return json.dumps(formatted_msg)


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
