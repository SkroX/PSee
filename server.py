# import the socketserver module of Python

import socketserver
import mss
 

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
            with mss.mss() as sct:
                file = sct.shot(output="img.jpg")
                sct.save(file)
            file = open('img.jpg', 'rb')
            content = file.read()
            size = len(content)
            size = "%018d" % size
            print (size)
            self.wfile.write(size.encode())
            self.wfile.write(content)
            file.close()                                            
# Create a TCP Server instance

aServer = socketserver.TCPServer(('', 9010), MyTCPRequestHandler, bind_and_activate=True)

 

# Listen for ever

aServer.serve_forever()
