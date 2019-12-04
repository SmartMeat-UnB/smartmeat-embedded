import RPi.GPIO as GPIO
import time
from gpiozero import LED, Button
import os


class RaspGPIO:
    def state_sticks():
        # Nao esquecer de alterar para os pinos da rasp
        slot1 = 11
        slot2 = 13
        slot3 = 12
        slot4 = 7
        # Definindo constantes dos motores
        # motor1 = 31
        # motor2 = 22
        # motor3 = 29
        # motor4 = 15

        sticker1 = False
        sticker2 = False
        sticker3 = False
        sticker4 = False

        # GPIO.setmode(GPIO.BCM)
        # BCM significa que estamos utilizando pelo numero GPIO
        # Caso queira usar pelo numero da porta basta comentar a linha de cima e descomentar a de baixo
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # Estao definidos resistores de pull ups externos. Ou seja, sempre 5 e fecha quando o botao for pressionado
        GPIO.setup(slot1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(slot2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(slot3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(slot4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # GPIO para os motores
        # GPIO.setup(motor1, GPIO.OUT)
        # GPIO.setup(motor2, GPIO.OUT)
        # GPIO.setup(motor3, GPIO.OUT)
        # GPIO.setup(motor4, GPIO.OUT)

        # Iniciando os motores com dutyCycle igual a 0
        # Ou seja desligados
        # pwmMot1 = GPIO.PWM(motor1, 100)
        # pwmMot1.start(0)

        # pwmMot2 = GPIO.PWM(motor2, 100)
        # pwmMot2.start(0)

        # pwmMot3 = GPIO.PWM(motor3, 100)
        # pwmMot3.start(0)

        # pwmMot4 = GPIO.PWM(motor4, 100)
        # pwmMot4.start(0)

        if GPIO.input(slot1) == True:
            sticker1 = True
            # pwmMot1.ChangeDutyCycle(35)
            # pwmMot1.start(30)
            # time.sleep(4)
        elif GPIO.input(slot1) == False:
            sticker1 = False
            # pwmMot1.ChangeDutyCycle(0)

        if GPIO.input(slot2) == True:
            sticker2 = True
            # pwmMot2.ChangeDutyCycle(60)
            # pwmMot2.start(60)
            # time.sleep(4)
        elif GPIO.input(slot2) == False:
            sticker2 = False
            # pwmMot2.ChangeDutyCycle(0)

        if GPIO.input(slot3) == True:
            sticker3 = True
            # pwmMot3.ChangeDutyCycle(50)
            # pwmMot3.start(50)
            # time.sleep(4)
        elif GPIO.input(slot3) == False:
            sticker3 = False
            # pwmMot3.ChangeDutyCycle(0)

        if GPIO.input(slot4) == True:
            sticker4 = True
            # pwmMot4.ChangeDutyCycle(35)
            # pwmMot4.start(55)
            # time.sleep(4)
        elif GPIO.input(slot4) == False:
            sticker4 = False
            # pwmMot4.ChangeDutyCycle(0)

        print("\nSticker 1 = ", sticker1)
        print("\nSticker 2 = ", sticker2)
        print("\nSticker 3 = ", sticker3)
        print("\nSticker 4 = ", sticker4)
        print("===================")
        # time.sleep(0.5)
        sticks = [sticker1, sticker2, sticker3, sticker4]
        return sticks

    def state_temperature(temperature):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        valor2 = 0
        tempo = 0
        entrada = 16  # pin 16
        saida = 18  # pin 18
        GPIO.setup(saida, GPIO.OUT)
        GPIO.output(saida, False)
        GPIO.setup(entrada, GPIO.IN)

        microseconds = 0.00001 * float(tempo)
        time.sleep(microseconds)
        GPIO.output(saida, True)
        time.sleep(0.001)
        GPIO.output(saida, False)

        GPIO.add_event_detect(entrada, GPIO.RISING, callback=state_temperature)

        # while True:
        valor = temperature
        print(valor)
        if valor == 0:
            valor2 = 800
        if valor == 1:
            valor2 = 70
        if valor == 2:
            valor2 = 20
        if valor == 3:
            valor2 = 0
        print(valor2)
        tempo = 90 * valor2
        time.sleep(0.005)

