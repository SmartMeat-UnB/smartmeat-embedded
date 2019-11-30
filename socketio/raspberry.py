import RPi.GPIO as GPIO
import time


class RaspGPIO:
    def state_sticks():
        # Nao esquecer de alterar para os pinos da rasp
        slot1 = 12
        slot2 = 7
        slot3 = 13
        slot4 = 11

        # Constantes para o PWM
        dc1 = 0
        dc2 = 0
        dc3 = 0
        dc4 = 0

        # GPIO.setmode(GPIO.BCM)
        # BCM significa que estamos utilizando pelo numero GPIO
        # Caso queira usar pelo numero da porta basta comentar a linha de cima e descomentar a de baixo
        GPIO.setmode(GPIO.BOARD)

        # Estao definidos resistores de pull ups externos. Ou seja, sempre 5 e fecha quando o botao for pressionado
        GPIO.setup(slot1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(slot2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(slot3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(slot4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # GPIO para os motores
        GPIO.setup(33, GPIO.OUT)
        GPIO.setup(35, GPIO.OUT)
        GPIO.setup(38, GPIO.OUT)
        GPIO.setup(40, GPIO.OUT)

        # Iniciando os motores e
        pwmMot1 = GPIO.PWM(38, 100)
        pwmMot1.start(0)

        pwmMot2 = GPIO.PWM(33, 100)
        pwmMot2.start(0)

        pwmMot3 = GPIO.PWM(35, 100)
        pwmMot3.start(0)

        pwmMot4 = GPIO.PWM(40, 100)
        pwmMot4.start(0)

        GPIO.setwarnings(False)

        # while True:
        if GPIO.input(slot1) == True:
            x = True
            pwmMot1.ChangeDutyCycle(dc1)
            time.sleep(0.05)
            dc1 = dc1 + 1
            if dc1 == 100:
                dc1 = 0

        elif GPIO.input(slot1) == False:
            x = False

        if GPIO.input(slot2) == True:
            y = True
            pwmMot2.ChangeDutyCycle(dc1)
            time.sleep(0.05)
            dc1 = dc1 + 1
            if dc1 == 100:
                dc1 = 0

        elif GPIO.input(slot2) == False:
            y = False

        if GPIO.input(slot3) == True:
            z = True
            pwmMot3.ChangeDutyCycle(dc1)
            time.sleep(0.05)
            dc1 = dc1 + 1
            if dc1 == 100:
                dc1 = 0

        elif GPIO.input(slot3) == False:
            z = False

        if GPIO.input(slot4) == True:
            w = True
            pwmMot1.ChangeDutyCycle(dc1)
            time.sleep(0.05)
            dc1 = dc1 + 1
            if dc1 == 100:
                dc1 = 0

        elif GPIO.input(slot4) == False:
            w = False

        # print("\nSticker 1 = ", x)
        # print("\nSticker 2 = ", y)
        # print("\nSticker 3 = ", z)
        # print("\nSticker 4 = ", w)
        # print("===================")
        time.sleep(1)

        sticks = [x, y, z, w]
        return sticks
