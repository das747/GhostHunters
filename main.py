# подключение модульных программ
from Speaker import talk
from ArduinoUART import PySerial
from digit_recognizer import get_digit
from Bluetooth import add_client, get_confirmation
# подключение пакетов
import argparse
from time import sleep
from imutils.video import VideoStream
from keras.models import load_model
import sys
from bluetooth import BluetoothSocket, RFCOMM  # модуль pybluez

PORT = '/dev/ttyUSB0'  # порт ардуины

box_n = 0  # хранение номера коробки

# подключение к микрофону
server = BluetoothSocket(RFCOMM)
client = add_client(server, 3)
print('connected to microphone')

# подключение к ардуино
ser = PySerial(PORT)
print('connected to arduino')

model = load_model('mnist_trained_model.h5')  # загрузка модели CNN

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# захват видеопотока
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
sleep(1.0)

print('ready')
while True:
    sample = client.recv(32).decode()  # получаем строку с командой

    #  обработка ввода номера коробки
    if sample.isdigit():
        box_n = int(sample)
        talk('guv ' * box_n)
        ser.write_int(box_n)  # для отладки ардуино пищит

    # обработка команды искать
    elif 'forward' in sample:
        correct = 0
        while not correct:  # цикл поиска нужной коробки
            # пока не найдёт будет ездить по кругу
            for i in range(4):
                ser.write_command('forwards')  # отправляем команду "доехать до следующей коробки"
                while not ser.in_waiting:  # ожидание входящего сообщения
                    pass
                ser.read_int()
                if get_digit(vs, model) == box_n:  # если найдена нужная коробка
                    if get_confirmation(client):  # запрашиваем голосовое подтверждение
                        correct = 1
                        break
            ser.write_command('return')  # возврат на исходную позицию
        box_n = 0

    # завершение работы
    elif 'stop' in sample:
        sys.exit()

    elif 'name' in sample:
        talk('juja')
