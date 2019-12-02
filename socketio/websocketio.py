import socketio
import json
import random
import os
import time
import logging
import sys

from pytz import timezone
from datetime import datetime
from aiohttp import web
from smartmeat import Smartmeat


logger = logging.getLogger()
logger.setLevel(logging.INFO)

SIMULATOR = False
SLEEP_TIME = 2

sio = socketio.AsyncServer(logger=True, async_mode="aiohttp")
app = web.Application()
sio.attach(app)


global bbq
logger.info("Smartmeat created!")
bbq = Smartmeat.instance()


def unserialize(json_str):
    global bbq

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
        bbq = Smartmeat.instance()

    # bbq.set_state(True)
    bbq.set_temperature(random.randint(1, 4))

    active_sticks = bbq.get_active_sticks()
    inactive_sticks = list(set([1,2,3,4]).symmetric_difference(set(active_sticks)))

    if active_sticks:
        for _ in active_sticks:
            to_deactivate = random.choice(active_sticks)
            bbq.remove_stick("stick{}".format(to_deactivate))
    if inactive_sticks:
        for _ in inactive_sticks:
            to_activate = random.choice(inactive_sticks)
            bbq.set_stick("stick{}".format(to_activate))

    return bbq


@sio.on('connect')
async def connect(sid, environ):
    global bbq
    if not bbq:
        bbq = Smartmeat.instance()
    logger.info("Connected at {}".format(sid))
    await send_data()


@sio.on('message')
async def get_message(sid, data):
    global bbq
    # Fill BBQ attributes
    bbq = unserialize(data)
    logger.info("Message Received from {} containing: {}".format(sid, data))
    # shuffle new data into attributes
    if SIMULATOR:
        # if simulator, then send data back after shuffling
        logger.info("Simulator True! Shuffling data!")
        bbq = shuffle_data()
        #time.sleep(2)
        await send_data()


async def send_data(threaded=False):
    global bbq
    if not bbq:
        bbq = Smartmeat.instance()
    tz = timezone('Brazil/East')
    logger.info("Sending Message. Message time: {}".format(datetime.now(tz=tz)))
    msg = bbq.serialize()
    if threaded:
        while True:
            await sio.sleep(SLEEP_TIME)
            bbq = shuffle_data()
            msg = bbq.serialize()
            await sio.emit("message", msg)
    else:
        await sio.emit("message", msg)


@sio.event
def disconnect(sid):
    global bbq
    bbq = None
    logger.info('Disconnected {}'.format(sid))


if __name__ == '__main__':
    sio.start_background_task(send_data, threaded=True)
    web.run_app(app, host='0.0.0.0', port=8080)
