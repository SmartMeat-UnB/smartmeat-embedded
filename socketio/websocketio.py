import socketio
import json
import random
import os
import time
import logging
import sys
import RPi.GPIO as gpio

from datetime import datetime
from aiohttp import web
from smartmeat import Smartmeat
from raspberry import RaspGPIO

#gpio.setmode(gpio.BOARD)
#
#gpio.setup(29, gpio.OUT)
#gpio.setup(15, gpio.OUT)
#gpio.setup(22, gpio.OUT)
#gpio.setup(31, gpio.OUT)
#
#gpio.output(29, F)
#gpio.output(15, False)
#gpio.output(22, False)
#gpio.output(31, False)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SIMULATOR = False

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


def update():
    global bbq
    init_sticks = RaspGPIO.state_sticks()

    for i, value in enumerate(init_sticks):
    #    if value:
        bbq.set_stick("stick{}".format(i + 1))


def shuffle_data():
    global bbq

    bbq.set_state(True)
    bbq.set_temperature(random.randint(1, 4))

    active_sticks = bbq.get_active_sticks()
    inactive_sticks = list(set([1, 2, 3, 4]).symmetric_difference(set(active_sticks)))

    if active_sticks:
        for _ in active_sticks:
            to_deactivate = random.choice(active_sticks)
            bbq.remove_stick("stick{}".format(to_deactivate))
    if inactive_sticks:
        for _ in inactive_sticks:
            to_activate = random.choice(inactive_sticks)
            bbq.set_stick("stick{}".format(to_activate))

    return bbq


@sio.on("connect")
def connect(sid, environ):
    global bbq
    if not bbq:
        bbq = Smartmeat.instance()
    logger.info("Connected at {}".format(sid))


@sio.on("message")
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
        msg = bbq.serialize()
        # time.sleep(2)
        await send_data(msg)
    else:
        update()
        msg = bbq.serialize()
        await send_data(msg)


async def send_data(msg):
    logger.info("Sending Message. Message time: {}".format(datetime.now()))
    await sio.emit("message", msg)


@sio.event
def disconnect(sid):
    global bbq
    bbq = None
    logger.info("Disconnected {}".format(sid))


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
