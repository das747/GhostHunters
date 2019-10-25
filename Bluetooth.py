from bluetooth import BluetoothSocket, RFCOMM  # пакет pybluez
import argparse

# словарь адресов серверов
addr_dict = {'pi5': 'B8:27:EB:9E:3D:92', 'red': 'B8:27:EB:AE:01:FF',
             'micro': 'B8:27:EB:4A:F7:21'}


# добавление клиента на сервер
def add_client(server, port, client_name=''):
    server.bind((client_name, port))  # настройка подключения клиента
    print('waiting for BT connection...')
    server.listen(1)  # ожидание 1 запроса на подключение
    client_socket, addr = server.accept()  # принимаем подключение
    # if client_addr != addr:  # проверяем что подключился нужный клиент
    #     client_socket = add_client(server, port, client_addr)
    return client_socket


# запрос голосового подтверждения
def get_confirmation(client):
    client.send(1)  # посылаем сигнал на микрофон
    return bool(int(client.recv().decode()))  # преобразуем ответ в логическое значение


#  тестовый код
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    # роль, по умолчанию поднимается сервер
    ap.add_argument("-m", "--mode", type=str, default="server",
                    help="open connection as server pr as client")
    # имя сервера из словаря addr_dict
    ap.add_argument("-n", "--name", type=str, default="red",
                    help="chose server name")
    args = vars(ap.parse_args())
    socket = BluetoothSocket(RFCOMM)
    # в режиме сервера печатаем входящие сообщения
    if args['mode'] == 'server':
        print('starting server...')
        client = add_client(socket, 3)
        print('connected')
        while True:
            data = client.recv(16)
            print(data.decode())  # преобразование из байт в строку
    # в режиме клиента отправляем введёные строки
    elif args['mode'] == 'client':
        print('connecting to ' + args['name'] + '...')
        socket.connect((addr_dict[args['name']], 3))
        print('connected')
        while True:
            socket.send(input())
