import selectors
import socket

sel = selectors.DefaultSelector()


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    try:
        data = conn.recv(1000)  # Should be ready
    except:
        print('closing 1', conn)
        sel.unregister(conn)
        conn.close()
    else:
        if data:
            print('echoing', repr(data), 'to', conn)
            conn.send(data)  # Hope it won't block
        else:
            print('closing 2', conn)
            sel.unregister(conn)
            conn.close()


sock = socket.socket()
sock.bind((socket.gethostname(), 12345))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    '''
    第一次: 会阻塞在select()这里, 
    解除阻塞: 当客户端调用connect方法时,解除阻塞,此时callback是本代码中的accept方法, 执行完之后,又阻塞在select
    第二次: 当客户端调用send发消息时, 解除阻塞, 此时callback是本代码中的read方法
    '''
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
