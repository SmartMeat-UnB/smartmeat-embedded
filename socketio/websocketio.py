import socketio
import json
import random
import os

from datetime import datetime
from aiohttp import web
from smartmeat import Smartmeat

import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

sio = socketio.AsyncServer(logger=True)
app = web.Application()
sio.attach(app)


def instantiate_smartmeat():
    logger.info("Instantiating object")
    #global bbq
    bbq = Smartmeat.instance()
    bbq.set_state(True)
    bbq.set_temperature(random.randint(100, 300))
#    bbq.sticks = [
#        {
#            "stick1": True,
#            "time_active": "{}:{}".format(random.randint(0, 60), random.randint(0, 60))
#        },
#        {
#            "stick2": False,
#            "time_active": "00:00"
#        },
#        {
#            "stick3": False,
#            "time_active": "00:00"
#        },
#        {
#            "stick4": True,
#            "time_active": "00:00"
#        }
#    ]

    return bbq


logger.info("Smartmeat created!")
bbq = instantiate_smartmeat()


def unserialize(json_str):
    #global bbq

    if not bbq:
        instantiate_smartmeat()

    # data = json.dumps(json_str)
    data = json_str
    data = data["smartmeat"]
    bbq.set_state(data["on"])
    bbq.set_temperature(data["temperature"])
    # bbq.set_stick(data["sticks1"])
    return bbq


async def index(request):
    """Serve the client-side application."""
    with open('./socketio/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
def connect(sid, environ):
    global bbq
    if not bbq:
        instantiate_smartmeat()
    logger.info("Connected {}".format(sid))


@sio.event
def message(sid, data):
    global bbq
    bbq = unserialize(data)
    logger.warn('BBQ message: {}'.format(bbq))
    
    sio.emit('my response', {'response': 'my response'})


@sio.event
def send_data(sid, json_str):
    logger.info('Sending data!')
    sio.emit(json_str)


@sio.event
def disconnect(sid):
    global bbq
    bbq = None
    logger.info('Disconnected {}'.format(sid))


# app.router.add_static('/static', 'static')
app.router.add_get('/', index)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
