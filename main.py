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

PORT = '/dev/ttyUSB1'
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

print('ready')
while True:
    sample = client.recv(32).decode()  # получаем строку с командой

    #  обработка ввода номера коробки
    if sample.isdigit():
        box_n = int(sample)
        talk('guv ' * box_n)
        ser.write_int(box_n)

    # обработка команды искать
    elif 'forward' in sample:
        correct = 0
        while not correct:
            # пока не найдёт будет ездить по кругу
            for box in range(4):
                ser.flushInput()
                ser.write_int(5)
                while not ser.in_waiting:
                    pass
                ser.read()
                digit = []
                for i in range(2):
                    for _ in range(5):
                        sleep(0.5)
                        digit.append(get_digit(vs, model))
                        
                    print(digit)
                #print(digit == box_n)
                if digit[1] == box_n:
                    correct = 1
                    break
            ser.write_command('return')
                
        talk('end')
        box_n = 0

    # завершение работы
    elif 'stop' in sample:
        sys.exit()

    elif 'name' in sample:
        talk('juja')
