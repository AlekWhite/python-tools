import socket
import pickle
from threading import Thread
global recentData

# sets up recentData
recentData = [-1, -1, -1]
print(recentData)

# sets up socket using ipv4 and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connects socket to an ip (host-ip/local-host) and port
s.bind((socket.gethostname(), 6591))
s.listen(5)


def mainLoop(name):

    # listen for connections and accept them
    while True:

        # accept the foreign connection
        clientsocket, addresss = s.accept()
        print("\n")
        print(f"connection from {addresss} has been established ")

        # sends the connection a string, using utf-8 bytes
        clientsocket.send("connected".encode())

        # waits for the clients message
        fullData = b""
        newData = True
        while True:

            # receives part of the data
            data = clientsocket.recv(16)

            # look for data len in the header
            if newData and (data != ""):
                dataLen = int(data[:10])
                newData = False

            # appends the new data to the main stream
            fullData += data

            # detects when all data has been received
            if len(fullData)-10 == dataLen:

                # turns data into an object
                obj = pickle.loads(fullData[10:])
                print(obj)

                # var used by other scrips
                recentData = fullData

                # clears data to prep for new data
                fullData = b""
                newData = True
                clientsocket.close()
                break

threadMAIN = Thread(target=mainLoop, args="2")
threadMAIN.start()