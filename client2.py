import socket
import time

s = socket.socket()
host = socket.gethostname()
print(host)

port = 12345

s.connect((host, port))
for i in range(20, 40):
    time.sleep(1)
    msg = str(i)
    s.send(msg.encode('utf8'))
    print(s.recv(1024).decode('utf8'))

s.send('break'.encode('utf8'))
s.close()

