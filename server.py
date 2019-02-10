# import the socketserver module of Python

import socketserver
import pyscreenshot as ps
import matplotlib.image as img
import json
 

# Create a Request Handler

# In this TCP server case - the request handler is derived from StreamRequestHandler

class MyTCPRequestHandler(socketserver.StreamRequestHandler):

 

# handle() method will be called once per connection

    def handle(self):

        # Receive and print the data received from client

        print("Recieved one request from {}".format(self.client_address[0]))

        msg = self.rfile.readline().strip()

        print("Data Recieved from client is:".format(msg))

        print(msg)  

        # Send some data to client
        while True: 
            im = ps.grab()
            im.save('sa.png')
            file = open('sa.png', 'rb')
            content = file.read()
            size = len(content)
            size = "%018d" % size
            print (size)
            self.wfile.write(size.encode())
            self.wfile.write(content)
            file.close()                                            
# Create a TCP Server instance

aServer = socketserver.TCPServer(('', 9000), MyTCPRequestHandler, bind_and_activate=True)

 

# Listen for ever

aServer.serve_forever()
