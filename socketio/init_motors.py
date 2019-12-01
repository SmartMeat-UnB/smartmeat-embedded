import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

gpio.setup(29, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(31, gpio.OUT)

gpio.output(29, True)
gpio.output(15, True)
gpio.output(22, True)
gpio.output(31, True)


