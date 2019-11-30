
import qrcode
# import pygame
import netifaces as ni
import matplotlib.pyplot as plt
# from pygame.locals import *


def format_ipaddr(ipaddr):
    return "http://{}:8080".format(ipaddr)


def get_ipaddr():
    network_interface = ''
    ip = ni.ifaddresses(network_interface)[ni.AF_INET][0]['addr']
    return format_ipaddr(ip)


def get_qrcode_image():
    ipaddr = get_ipaddr()
    img = qrcode.make(ipaddr)
    return img


# def display_image(img):
#     pygame.init()
#     WIDTH = 256
#     HEIGHT = 256
#     windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0)
#     img = get_qrcode_image()
#     windowSurface.blit(img, (0, 0))
#     pygame.display.flip()


def plot_image():
    img = get_qrcode_image()
    plt.imshow(img)
    plt.show()


plot_image()