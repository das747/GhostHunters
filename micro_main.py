# подключение из модульных программ
from Speaker import *
from Bluetooth import addr_dict
# подключение пакетов
from bluetooth import BluetoothSocket, RFCOMM  # пакет pybluez
import argparse
import sys


talk("wuuuuf")

ap = argparse.ArgumentParser()
# метод распознавания
ap.add_argument('-r', "--recognizer", type=str, default='sphinx',
                help="recognizer type, google or sphinx")
# имя bluetooth сервера
ap.add_argument("-n", "--name", type=str, default="red",
                help="chose server name")
args = vars(ap.parse_args())

# подключение к серверу
print('connecting to ' + args['name'] + '...')
client = BluetoothSocket(RFCOMM)
client.connect((addr_dict[args['name']], 3))
print('connected')

box_n = 0

while True:
    sample = get_command(args['recognizer'])  # получаем строку с командой

    #  обработка ввода номера коробки
    if any([com in sample for com in box_com]):
        for i in range(4):
            if any([com in sample for com in num_coms[i]]):
                box_n = i + 1
                break
        client.send(str(box_n))  # отправляем номер коробки жуже
        talk('guv ' * box_n)  # озвучиваем в наушники номер коробки

    # обработка команды искать
    elif 'forward' in sample:
        client.send("forward")  # отправляем команду жуже
        talk('вперёд')
        complete = 0
        while not complete:  # дублирование цикла поиска коробки у жужи
            client.recv()  # по команде запрашиваем голосовое подтверждение
            complete = get_confirmation(args['recognizer'])
            client.send(complete)  # отправляем ответ жуже

        box_n = 0

    # завершение работы
    elif 'stop' in sample:
        client.send("stop")
        talk("Shutting down")
        sys.exit()

    elif 'name' in sample:
        talk("My name is Juja")
