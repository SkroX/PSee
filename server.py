import socketserver
import mss
import lzma
import pygame
from threading import Thread


class ScreenshotHandler(socketserver.StreamRequestHandler):

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

class MouseHandler(socketserver.StreamRequestHandler):

    def handle(self):
        with open("hello from the other thread", "w") as f:
            f.write('hi!')
        print("fdjaklfjdasklsjafdskdljaslkfjaksl;jfdklsafjdkljasdl;fkjfas;l")
        print(self.rfile.read())

# Create a TCP Server instance
ScreenshotServer = socketserver.TCPServer(('', 9000), ScreenshotHandler, bind_and_activate=True)
MouseServer = socketserver.TCPServer(('', 9001), ScreenshotHandler, bind_and_activate=True)

# Listen for ever
print("Starting server!")
screenshot_thread = Thread(target=ScreenshotServer.serve_forever)
screenshot_thread.start()
MouseServer.serve_forever()

