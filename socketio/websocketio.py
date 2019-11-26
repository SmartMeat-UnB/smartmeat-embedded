import socketio
import json
import random
import os
import time
import logging
import sys

from datetime import datetime
from aiohttp import web
from smartmeat import Smartmeat


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

sio = socketio.AsyncServer(logger=True, async_mode="aiohttp")
app = web.Application()
sio.attach(app)


def instantiate_smartmeat():
    logger.info("Instantiating object")
    #global bbq
    bbq = Smartmeat.instance()
    bbq.set_state(True)
    bbq.set_temperature(random.randint(1, 4))
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
    global bbq

    if not bbq:
        bbq = instantiate_smartmeat()

    # data = json.dumps(json_str)
    data = json_str
    data = data["smartmeat"]
    bbq.set_state(data["on"])
    bbq.set_temperature(data["temperature"])
    # bbq.set_stick(data["sticks1"])
    return bbq


def shuffle_data():
    global bbq

    if not bbq:
        bbq = instantiate_smartmeat()

    # bbq.set_state(True)
    bbq.set_temperature(random.randint(1, 4))

    active_sticks = bbq.get_active_sticks()
    inactive_sticks = list(set([1,2,3,4]).symmetric_difference(set(active_sticks)))

    if active_sticks:
        to_deactivate = random.choice(active_sticks)
        bbq.remove_stick("stick{}".format(to_deactivate))
    if inactive_sticks:
        to_activate = random.choice(inactive_sticks)
        bbq.set_stick("stick{}".format(to_activate))

    return bbq


async def index(request):
    """Serve the client-side application."""
    with open('./socketio/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
def connect(sid, environ):
    global bbq
    if not bbq:
        bbq = instantiate_smartmeat()
    logger.info("Connected {}".format(sid))


@sio.event
async def message(sid, data):
    global bbq
    # fill bbq attributes
    bbq = unserialize(data)
    time.sleep(2)
    # shuffle new data into attributes
    bbq = shuffle_data()
    # format object in JSON
    msg = bbq.serialize()
    # emit message with new BBQ information
    await sio.emit("message", msg) 


# TODO sending is not working when using this function
async def send_data(sid):
    global bbq
    logger.info('Sending data!')
    # format object in JSON
    msg = bbq.serialize()
    # emit message with new BBQ information
    await sio.emit("message", msg) 


@sio.event
def disconnect(sid):
    global bbq
    bbq = None
    logger.info('Disconnected {}'.format(sid))


# app.router.add_static('/static', 'static')
app.router.add_get('/', index)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
