from bluetooth import *
import sys


def add_client(server, port, client_addr, client_name=''):
    server.bind(client_name, port)
    server.listen(1)
    client_socket, addr = server.accept()
    # if client_addr != addr:
    #     client_socket = add_client(server, port, client_addr)
    return client_socket


def get_confirmation(client):
    client.send(1)
    return bool(int(client.recv().decode()))


if __name__ == '__main__':
    CLIENT = sys.argv[1]
    server = BluetoothSocket(RFCOMM)
    client = add_client(server, 3, CLIENT)
    while True:
        data = client.recv(16)
        print(data)
