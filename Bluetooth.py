from bluetooth import *
import argparse


def add_client(server, port, client_name=''):
    server.bind((client_name, port))
    server.listen(1)
    client_socket, addr = server.accept()
    # if client_addr != addr:
    #     client_socket = add_client(server, port, client_addr)
    return client_socket


def get_confirmation(client):
    client.send(1)
    return bool(int(client.recv().decode()))


if __name__ == '__main__':
    addr_dict = {'pi5':'B8:27:EB:9E:3D:92', 'red':'B8:27:EB:AE:01:FF', 'micro':'B8:27:EB:4A:F7:21'}
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--mode", type=str, default="server",
                    help="open connection as server pr as client")
    ap.add_argument("-n", "--name", type=str, default="red",
                    help="chose server name")
    args = vars(ap.parse_args())
    socket = BluetoothSocket(RFCOMM)
    if args['mode'] == 'server':
        print('starting server...')
        client = add_client(socket, 3)
        print('connected')
        while True:
            data = client.recv(16)
            print(data.decode())
    elif args['mode'] == 'client':
        socket.connect((addr_dict[args['name']], 3))
        print('connected')
        while True:
            socket.send(input())
