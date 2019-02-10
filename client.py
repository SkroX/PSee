import socket
import sys
import pygame

HOST, PORT = "127.0.0.1", 9000
data = " ".join(sys.argv[1:])
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption('PSee')
white = (255, 64, 64)

def get_image_from_server(sock):
    with open ('screennew.png', 'wb') as f:
        size = int(sock.recv(18).decode('utf-8'))
        print("size of image: ", size)
        received = b''
        while size > 0:
            r = sock.recv(size)
            size -= len(r)
            received += r
        print("Received: {}".format(len(received)))
        f.write(received)

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))
    # Receive data from the server and shut down
    while True:
        get_image_from_server(sock)
        img = pygame.image.load('screennew.png')
        screen.fill((white))
        img = pygame.transform.scale(img, (1600, 900))
        screen.blit(img, (0,0))
        pygame.display.flip()
print("Sent:     {}".format(data))

