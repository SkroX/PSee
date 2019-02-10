import socket
import sys
import pygame
import time
import lzma

#HOST, PORT = "192.168.43.244", 9010
HOST, PORT = "127.0.0.1", 9012
RESOLUTION = (1366, 768)
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

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # Receive data from the server and shut down
    file = open('screennew.png', 'wb')
    while True:
        get_image_from_server(sock, file)
        img = pygame.image.load('screennew.png')
        screen.fill((white))
        screen.blit(img, (0,0))
        pygame.display.flip()
