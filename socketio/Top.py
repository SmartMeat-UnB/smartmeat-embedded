import RPi.GPIO as GPIO
import time
import os
from threading import Thread
from websocketio import set_temp_rasp


def triac(temperatura):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    valor2 =0
    tempo = 0
    entrada = 16 #pin 16
    saida = 18 #pin 18
    GPIO.setup(saida, GPIO.OUT)
    GPIO.output(saida, False)
    GPIO.setup(entrada, GPIO.IN)
                
    def acende(a):
        microseconds = 0.00001*float(tempo)
        time.sleep(microseconds)
        GPIO.output(saida, True)
        time.sleep(0.001)
        GPIO.output(saida, False)
        

    GPIO.add_event_detect(entrada, GPIO.RISING, callback=acende)

while True:
    valor = temperatura
    print(valor)
    if(valor == 0):
        valor2 = 800
    if(valor == 1):
        valor2 = 70
    if(valor == 2):
        valor2 = 20
    if(valor == 3):
        valor2 = 0
    print(valor2)
    tempo = (90*valor2)
    time.sleep(0.005)
#Definindo funcao para deteccao dos slots e ativacao dos motores
def mainBTN ():

    def mainTermo():
        import RPi.GPIO as gpio
        CLK1 = 33
        DBIT1 = 35 #S0
        CS1 = 37

        CLK2 = 36
        DBIT2 = 38 #S0
        CS2 = 40


        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(False)
        gpio.setup(CLK1, gpio.OUT)
        gpio.setup(DBIT1, gpio.IN)
        gpio.setup(CS1, gpio.OUT)
        gpio.setup(CLK2, gpio.OUT)
        gpio.setup(DBIT2, gpio.IN)
        gpio.setup(CS2, gpio.OUT)


        def Thermal_Couple_Read(CLK, DBIT, CS):
            value = 0
            #iniciar sensor
            gpio.output(CS, False)
            time.sleep(0.002)
            gpio.output(CS, True)
            time.sleep(0.2)

            #Ler o chip e retornar a temperatura
            gpio.output(CS, False)
            gpio.output(CLK, True)
            gpio.output(CLK, False)

            i = 14
            while i>= 0:
                gpio.output(CLK, True)
    ##            print("\nvalor1",value)
                value += gpio.input(DBIT) << i
    ##            print("\nValor 2", value)
                gpio.output(CLK, False)
                i = i-1

            #if((value & 0x04)==0x04):
                #return -1

            return value >> 3
                
        SENSOR_VALUE1 = 0
        SENSOR_VALUE2 = 0
        x = 1
        i=0

        gpio.output(CS1, True)
        gpio.output(CLK1, False)
        gpio.output(CS2, True)
        gpio.output(CLK2, False)
        
        SENSOR_VALUE1 = Thermal_Couple_Read(CLK1, DBIT1, CS1)
        #print("\nS1: ", SENSOR_VALUE1)
        SENSOR_VALUE2 = Thermal_Couple_Read(CLK2, DBIT2, CS2)
        #print("\nS2: ", SENSOR_VALUE2)

        Ctemp1 = SENSOR_VALUE1*0.25
        Ctemp2 = SENSOR_VALUE2*0.25
        print("===================")
        #print("\nTemperatura 1 = ", Ctemp1)
        #print("\nTemperatura 2 = ", Ctemp2)
        #CtempMedia = (Ctemp1+Ctemp2)/2
        print("\nTemperatura Media = ", Ctemp2)
    
    #Nao esquecer de alterar para os pinos da rasp
    slot1 = 11
    slot2 = 13
    slot3 = 12
    slot4 = 7

    #Definindo constantes dos motores
    motor1 = 31 
    motor2 = 22
    motor3 = 29 
    motor4 = 15 

    #Inicializa os stickers
    sticker1=False
    sticker2=False
    sticker3=False
    sticker4=False

    #Constantes para o PWM
    dc1 = 0
    dc2  = 0
    dc3 = 0
    dc4 = 0
    
    #GPIO.setmode(GPIO.BCM)
    # BCM significa que estamos utilizando pelo numero GPIO
    # Caso queira usar pelo numero da porta basta comentar a linha de cima e descomentar a de baixo
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)


    #Estao definidos resistores de pull ups externos. Ou seja, sempre 5 e fecha quando o botao for pressionado
    GPIO.setup(slot1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(slot2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(slot3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(slot4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    #GPIO para os motores
    GPIO.setup(motor1, GPIO.OUT)
    GPIO.setup(motor2, GPIO.OUT)
    GPIO.setup(motor3, GPIO.OUT)
    GPIO.setup(motor4, GPIO.OUT)

    #Iniciando os motores com dutyCycle igual a 0
    #Ou seja desligados 
    pwmMot1 = GPIO.PWM(motor1,100)
    pwmMot1.start(0)    
     
    pwmMot2 = GPIO.PWM(motor2,100)
    pwmMot2.start(0)

    pwmMot3 = GPIO.PWM(motor3,100)
    pwmMot3.start(0)

    pwmMot4 = GPIO.PWM(motor4,100)
    pwmMot4.start(0)


    while True:
##        os.system('clear') or None

        if (GPIO.input(slot1) == True):
            sticker1=True
            pwmMot1.ChangeDutyCycle(35)
        

        elif (GPIO.input(slot1) == False):
            sticker1=False
            pwmMot1.ChangeDutyCycle(0)
            
        if (GPIO.input(slot2) == True):
            sticker2=True
            pwmMot2.ChangeDutyCycle(55)

        elif (GPIO.input(slot2) == False):
            sticker2=False
            pwmMot2.ChangeDutyCycle(0)
            
        if (GPIO.input(slot3) == True):
            sticker3=True
            pwmMot3.ChangeDutyCycle(35)
        
                                   
        elif (GPIO.input(slot3) == False):
            sticker3=False
            pwmMot3.ChangeDutyCycle(0)
            
        if (GPIO.input(slot4) == True):
            sticker4=True
            pwmMot4.ChangeDutyCycle(35)

                    
        elif (GPIO.input(slot4) == False):
            sticker4=False
            pwmMot4.ChangeDutyCycle(0)

        mainTermo()
        print("\nSticker 1 = ", sticker1)
        print("\nSticker 2 = ", sticker2)
        print("\nSticker 3 = ", sticker3)
        print("\nSticker 4 = ", sticker4)
        print("===================")
        time.sleep(0.5)


controle = Thread(target=triac,args=set_temp_rasp())
mainBTN()
