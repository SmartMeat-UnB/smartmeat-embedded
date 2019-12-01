import RPi.GPIO as GPIO
import time
from gpiozero import LED, Button
import os


class RaspGPIO:

    # Constantes para o PWM
    dc1 = 0
    dc2 = 0
    dc3 = 0
    dc4 = 0
    # Constantes para o Sensor
    SENSOR_VALUE1 = 0
    SENSOR_VALUE2 = 0

    def Thermal_Couple_Read(CLK, DBIT, CS):
        value = 0
        # iniciar sensor
        gpio.output(CS, False)
        time.sleep(0.002)
        gpio.output(CS, True)
        time.sleep(0.2)

        # Ler o chip e retornar a temperatura
        gpio.output(CS, False)
        gpio.output(CLK, True)
        gpio.output(CLK, False)

        i = 14
        while i >= 0:
            gpio.output(CLK, True)
            ##            print("\nvalor1",value)
            value += gpio.input(DBIT) << i
            ##            print("\nValor 2", value)
            gpio.output(CLK, False)
            i = i - 1

        # if((value & 0x04)==0x04):
        # return -1

        return value >> 3

    # Definindo funcao para deteccao dos slots e ativacao dos motores
    def mainTermo():

        CLK1 = 33
        DBIT1 = 35  # S0
        CS1 = 37

        CLK2 = 36
        DBIT2 = 38  # S0
        CS2 = 40

        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(False)
        gpio.setup(CLK1, gpio.OUT)
        gpio.setup(DBIT1, gpio.IN)
        gpio.setup(CS1, gpio.OUT)
        gpio.setup(CLK2, gpio.OUT)
        gpio.setup(DBIT2, gpio.IN)
        gpio.setup(CS2, gpio.OUT)

        x = 1
        i = 0

        gpio.output(CS1, True)
        gpio.output(CLK1, False)
        gpio.output(CS2, True)
        gpio.output(CLK2, False)

        SENSOR_VALUE1 = Thermal_Couple_Read(CLK1, DBIT1, CS1)
        # print("\nS1: ", SENSOR_VALUE1)
        SENSOR_VALUE2 = Thermal_Couple_Read(CLK2, DBIT2, CS2)
        # print("\nS2: ", SENSOR_VALUE2)

        Ctemp1 = SENSOR_VALUE1 * 0.25
        Ctemp2 = SENSOR_VALUE2 * 0.25
        print("===================")
        print("\nTemperatura 1 = ", Ctemp1)
        print("\nTemperatura 2 = ", Ctemp2)
        CtempMedia = (Ctemp1 + Ctemp2) / 2
        print("\nTemperatura Media = ", CtempMedia)

        # Inicializa os stickers
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
        GPIO.setup(motor1, GPIO.OUT)
        GPIO.setup(motor2, GPIO.OUT)
        GPIO.setup(motor3, GPIO.OUT)
        GPIO.setup(motor4, GPIO.OUT)
        GPIO.output(motor1, True)
        GPIO.output(motor2, True)
        GPIO.output(motor3, True)
        GPIO.output(motor4, True)

    def state_sticks():
        # while True:
        ##        os.system('clear') or None
        # Nao esquecer de alterar para os pinos da rasp
        slot1 = 12
        slot2 = 7
        slot3 = 13
        slot4 = 11
        # Definindo constantes dos motores
        motor1 = 29
        motor2 = 15
        motor3 = 22
        motor4 = 31

        # Iniciando os motores com dutyCycle igual a 0
        # Ou seja desligados
        pwmMot1 = GPIO.PWM(motor1, 100)
        pwmMot1.start(100)

        pwmMot2 = GPIO.PWM(motor2, 100)
        pwmMot2.start(100)

        pwmMot3 = GPIO.PWM(motor3, 100)
        pwmMot3.start(100)

        pwmMot4 = GPIO.PWM(motor4, 100)
        pwmMot4.start(100)

        if GPIO.input(slot1) == True:
            sticker1 = True
            pwmMot1.ChangeDutyCycle(65)

        elif GPIO.input(slot1) == False:
            sticker1 = False
            pwmMot1.ChangeDutyCycle(100)

        if GPIO.input(slot2) == True:
            sticker2 = True
            pwmMot2.ChangeDutyCycle(55)

        elif GPIO.input(slot2) == False:
            sticker2 = False
            pwmMot2.ChangeDutyCycle(100)

        if GPIO.input(slot3) == True:
            sticker3 = True
            pwmMot3.ChangeDutyCycle(65)

        elif GPIO.input(slot3) == False:
            sticker3 = False
            pwmMot3.ChangeDutyCycle(100)

        if GPIO.input(slot4) == True:
            sticker4 = True
            pwmMot4.ChangeDutyCycle(65)

        elif GPIO.input(slot4) == False:
            sticker4 = False
            pwmMot4.ChangeDutyCycle(100)

        mainTermo()
        print("\nSticker 1 = ", sticker1)
        print("\nSticker 2 = ", sticker2)
        print("\nSticker 3 = ", sticker3)
        print("\nSticker 4 = ", sticker4)
        print("===================")
        time.sleep(0.5)
        sticks = [sticker1, sticker2, sticker3, sticker4]
        return sticks
