import socket
from threading import Thread

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))

s.listen(5)


def accept1(c):
    while True:
        msg = c.recv(1024)
        result = msg.decode('utf8')
        if result == 'break':
            break
        print(result)
        c.send(msg)


while True:
    # 阻塞: 当客户端代码s.connect((host, port))执行完之后,解除阻塞
    c, addr = s.accept()
    print(f'addr {addr}')
    # 给每个客户端分配一个线程
    t = Thread(target=accept1, args=(c, ))
    t.start()
