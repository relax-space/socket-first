import logging
import selectors
import socket

sel = selectors.DefaultSelector()


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    except:
        return '0.0.0.0'


def accept(sock, ip_port: str):
    try:
        conn, addr = sock.accept()  # Should be ready
        msg = f'connected: server {ip_port} ,client: {addr}'
        logging.info(msg)
        conn.send(msg.encode('utf8'))
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, read)
    finally:
        pass


def read(conn, ip_port):
    try:
        data: bytes = conn.recv(1000)  # Should be ready
        if data:
            data_str = data.upper()
            logging.info(f'echoing {repr(data_str)} from {conn}')
            d = data_str.strip().lower()
            if d == b'exit':
                sel.unregister(conn)
                conn.close()
                return
            conn.send(data_str)  # Hope it won't block
        else:
            logging.info(f'closing 2 {conn}')
            sel.unregister(conn)
            conn.close()
    except Exception as e:
        logging.info(f'closing 1 {conn} {e}')
        sel.unregister(conn)
        conn.close()


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    sock = socket.socket()
    # sock.bind((socket.gethostname(), 12345))
    ip_port = get_ip(), 5000
    sock.bind(ip_port)
    sock.listen(100)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)

    logging.info(f'{ip_port} is listened')

    params = {'ip_port': ip_port, 'rev_list': []}
    while True:
        '''
        第一次: 会阻塞在select()这里, 
        解除阻塞: 当客户端调用connect方法时,解除阻塞,此时callback是本代码中的accept方法, 执行完之后,又阻塞在select
        第二次: 当客户端调用send发消息时, 解除阻塞, 此时callback是本代码中的read方法
        '''
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, ip_port)


if __name__ == '__main__':
    main()
