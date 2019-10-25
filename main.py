from Speaker import talk
from ArduinoUART import PySerial
from digit_recognizer import get_digit
import argparse
from time import sleep
from imutils.video import VideoStream
from keras.models import load_model
import sys
from Bluetooth import add_client, get_confirmation
from bluetooth import *

PORT = '/dev/cu.usbserial-A9GJJD9P'
box_n = 0

server = BluetoothSocket(RFCOMM)
client = add_client(server, 3)
print('connected to microphone')

ser = PySerial(PORT)
print('connected to arduino')

model = load_model('mnist_trained_model.h5')  # import CNN model weight

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
sleep(1.0)

while True:
    sample = client.recv(32).decode()  # получаем строку с командой

    #  обработка ввода номера коробки
    if sample.isdigit():
        box_n = int(sample)
        talk('guv ' * box_n)

    # обработка команды искать
    elif 'forward' in sample:
        correct = 0
        while not correct:
            # пока не найдёт будет ездить по кругу
            for i in range(4):
                ser.write_command('forwards')
                while not ser.in_waiting:
                    pass
                ser.read_int()
                if get_digit(vs, model) == box_n:
                    if get_confirmation(client):
                        correct = 1
                        break
            ser.write_command('return')
        box_n = 0

    # завершение работы
    elif 'stop' in sample:
        sys.exit()

    elif 'name' in sample:
        talk('juja')
