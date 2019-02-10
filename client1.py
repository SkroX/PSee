import socket
import sys
import pygame
import time
import lzma
from threading import Thread
from pynput.mouse import Button, Controller

#HOST, PORT = "192.168.43.244", 9010
#HOST_SS, PORT_SS = "192.168.43.228", 9000
HOST_SS, PORT_SS = "127.0.0.1", 9000
#HOST_MP, PORT_MP = "192.168.43.228", 9001
HOST_MP, PORT_MP = "127.0.0.1", 9001
RESOLUTION = (640, 480)
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('PSee')
white = (255, 64, 64)

def get_image_from_server(sock, file):
    t = time.time()
    size = int(sock.recv(18).decode('utf-8'))
    print("size of image: ", size)
    received = b''
    while size > 0:
        r = sock.recv(size)
        size -= len(r)
        received += r
    print("Received: {}, time: {}".format(len(received), time.time() - t))
    file.write(lzma.decompress(received))
    file.seek(0)

def open_socket_for_mouse():
    print ("inside mouse controller")
    mouse = Controller()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST_MP, PORT_MP))
        while True:
            x = mouse.position[0]
            y = mouse.position[1]
            x = "%05d" % x
            y = "%05d" % y
            sock.sendall(x.encode())
            sock.sendall(y.encode())

t = Thread(target=open_socket_for_mouse)
t.start()

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST_SS, PORT_SS))
    # Receive data from the server and shut down
    file = open('screennew.jpg', 'wb')
    while True:
        get_image_from_server(sock, file)
        img = pygame.image.load('screennew.jpg')
        screen.fill((white))
        img = pygame.transform.scale(img, RESOLUTION)
        screen.blit(img, (0,0))
        pygame.display.flip()
        open_socket_for_mouse()
