import socket
import pickle
from datetime import datetime

# gets current time
def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    utime = 0
    for i in range(3):
        utime += int(current_time[0 + i * 3] + current_time[1 + i * 3]) * pow(60, 2 - i)
    return utime

# defines the data
obj = [0, 40, get_time()]
data = pickle.dumps(obj)

# sets up socket using ipv4 and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# tells the socket what to connect to, (ip and port)
s.connect(("67.247.200.249", 6591))

# receives the data sent from the server (1024 = size)
msg = s.recv(1024)

# decodes the message
print(msg.decode())

# adds a header to the data
fullData = f'{len(data):<10}'.encode() + data

# sends the data to the server
s.send(fullData)



