# import the socketserver module of Python

import socketserver
import mss
import lzma
import pygame


# Create a Request Handler

# In this TCP server case - the request handler is derived from StreamRequestHandler

class MyTCPRequestHandler(socketserver.StreamRequestHandler):

    def handle(self):
        # Receive and print the data received from client
        print("Received one request from {}".format(self.client_address[0]))
        # Send some data to client
        while True:
            with mss.mss() as sct:
                file = sct.shot(output="img.jpg")
                sct.save(file)
            img = pygame.image.load('img.jpg')
            img = pygame.transform.scale(img, (1366, 768))
            pygame.image.save(img, 'img.jpg')
            file = open('img.jpg', 'rb')
            data = file.read()

            content = lzma.compress(data)
            size = len(content)
            size = "%018d" % size
            print("orig: %d, compressed: %d" % (len(data), len(content)))
            self.wfile.write(size.encode())
            self.wfile.write(content)
            file.close()

# Create a TCP Server instance
aServer = socketserver.TCPServer(('', 9012), MyTCPRequestHandler, bind_and_activate=True)

# Listen for ever
print("Starting server!")
aServer.serve_forever()
