import RPi.GPIO as GPIO
import time


class RaspGPIO:
    def state_sticks():
        # GPIO.setmode(GPIO.BCM)
        # BCM significa que estamos utilizando pelo numero GPIO
        # Caso queira usar pelo numero da porta basta comentar a linha de cima e descomentar a de baixo
        GPIO.setmode(GPIO.BOARD)

        # Estao definidos resistores de pull ups externos. Ou seja, sempre 5 e fecha quando o botao for pressionado
        pin_7 = GPIO.setup(7, GPIO.IN)
        pin_11 = GPIO.setup(11, GPIO.IN)
        pin_12 = GPIO.setup(12, GPIO.IN)
        pin_13 = GPIO.setup(13, GPIO.IN)
        GPIO.setwarnings(False)

        sticks = [pin_7, pin_11, pin_12, pin_13]
        return sticks
