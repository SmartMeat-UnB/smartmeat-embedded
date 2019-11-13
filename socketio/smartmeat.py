import json
import random
import os
import logging
import logging
import sys

from datetime import datetime


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

MIN_TEMP = 0
MAX_TEMP = 400


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class Smartmeat():

    def __init__(self, state=False, temperature=-100, sticks=[None]):
        self.state = state
        self.temperature = temperature
        self.sticks = sticks


    def __str__(self):
        return self.format_msg()


    def set_state(self, state):
        if self.has_data():
            self.state = state
        else:
            logger.info("WARN: At least one attribute of SmartMeat is None")


    def set_temperature(self, value):
        if self.has_data():
            if value > MIN_TEMP and value < MAX_TEMP:
                self.temperature = value
            else:
                logger.info("ERROR: Invalid temperature value: {}".format(value))
        else:
            logger.info("WARN: At least one attribute of SmartMeat is None")


    def set_stick(self, stick_number, state, time_active):
        curr_time = datetime.now().time()
        if self.has_data():
            self.sticks[stick_number] = {
                "stick{}".format(stick_number): True,
                "time_active": curr_time
            }
        else:
            logger.info("WARN: At least one attribute of SmartMeat is None")


    def remove_stick(self, stick_number):
        if self.has_data():
            self.sticks[stick_number] = {
                "stick{}".format(stick_number): False,
                "time_active": "00:00"
            }
        else:
            logger.info("WARN: At least one attribute of SmartMeat is None")


    def has_data(self):
        #if not self.state:
        #    return False
        #if not self.temperature:
        #    return False
        #if not self.sticks:
        #    return False
        return True


    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


    def format_msg(self):
        formatted_msg = {}
        msg = self.serialize()
        formatted_msg["smartmeat"] = msg

        if not self.has_data():
            logger.info("WARN: At least one attribute of SmartMeat is None")

        logger.info("Formatted message: {}".format(formatted_msg))

        return json.dumps(formatted_msg)
