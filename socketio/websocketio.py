import socketio
import json
import random

from datetime import datetime
from aiohttp import web


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

MIN_TEMP = 50
MAX_TEMP = 400


class Smartmeat():

    def __init__(self, state=None, temperature=None, sticks=[]):
        self.state = state
        self.temperature = temperature
        self.sticks = sticks

    
    def __str__(self):
        return self.format_msg()


    def turn_on_smartmeat(self):
        if self.has_data():
            self.state = True
        else:
            print("WARN: At least one attribute of SmartMeat is None")


    def turn_off_smartmeat(self):
        if self.has_data():
            self.state = False
        else:
            print("WARN: At least one attribute of SmartMeat is None")


    def set_temperature(self, value):
        if self.has_data():
            if value > MIN_TEMP and value < MAX_TEMP:
                self.temperature = value
            else:
                print("ERROR: Invalid temperature value: {}".format(value))
        else:
            print("WARN: At least one attribute of SmartMeat is None")


    def set_stick(self, stick_number, state, time_active):
        curr_time = datetime.now().time()
        if self.has_data():
            self.sticks[stick_number] = {
                "stick{}".format(stick_number): True,
                "time_active": curr_time
            }
        else:
            print("WARN: At least one attribute of SmartMeat is None")


    def remove_stick(self, stick_number):
        if self.has_data():
            self.sticks[stick_number] = {
                "stick{}".format(stick_number): False,
                "time_active": "00:00"
            }
        else:
            print("WARN: At least one attribute of SmartMeat is None")


    def has_data(self):
        if not self.state:
            return False
        if not self.temperature:
            return False
        if not self.sticks:
            return False
        return True


    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


    def format_msg(self):
        formatted_msg = {}
        if self.has_data():
            msg = self.serialize()
            formatted_msg["smartmeat"] = msg
        else:
            print("WARN: At least one attribute of SmartMeat is None")

        print("Formatted message:", formatted_msg)

        return json.dumps(formatted_msg)


def instantiate_smartmeat():
    bbq = Smartmeat()
    bbq.state = True
    bbq.temperature = random.randint(100, 300)
    bbq = [
        {
            "stick1": True,
            "time_active": "{}:{}".format(random.randint(0, 60), random.randint(0, 60))
        },
        {
            "stick2": False,
            "time_active": "00:00"
        },
        {
            "stick3": False,
            "time_active": "00:00"
        },
        {
            "stick4": True,
            "time_active": "00:00"
        },
    ]


def sync_data(obj):
    """
    Sync attributes with data collected from sensors
    """
    pass 


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
