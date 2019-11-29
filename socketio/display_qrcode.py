
import qrcode
import pygame
import netifaces as ni
from pygame.locals import *


def get_ipaddr():
    network_interface = 'enp34s0'
    ip = ni.ifaddresses(network_interface)[ni.AF_INET][0]['addr']
    return ip


def get_qrcode_image():
    ipaddr = get_ipaddr()
    img = qrcode.make(ipaddr)
    return img


def display_image(img):
    pygame.init()
    WIDTH = 256
    HEIGHT = 256
    windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0)
    img = get_qrcode_image()
    windowSurface.blit(img, (0, 0))
    pygame.display.flip()
