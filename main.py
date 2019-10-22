from Speaker import *
from ArduinoUART import PySerial
from digit_recognizer import get_digit
import sys


PORT = '/dev/cu.usbserial-A9GJJD9P'
box_n = 0

talk("ввваф")
ser = PySerial(PORT)


while True:
    sample = get_command()  # получаем строку с командой

    #  обработка ввода номера коробки
    if any([com in sample for com in box_com]):
        for i in range(4):
            if any([com in sample for com in num_coms[i]]):
                box_n = i + 1
                break
        ser.write_int(box_n)
        talk('гав' * box_n)

    # обработка команды искать
    elif 'forward' in sample:
        talk('вперёд')
        correct = 0
        while not correct:
            # пока не найдёт будет ездить по кругу
            for i in range(4):
                ser.write_command('forwards')
                while not ser.in_waiting:
                    pass
                ser.read_int()
                if get_digit() == box_n:
                    if get_confirmation():
                        correct = 1
                        break
            ser.write_command('return')
        box_n = 0

    # завершение работы
    elif 'stop' in sample:
        talk("Да, конечно, гав гав")
        sys.exit()

    elif 'name' in sample:
        talk("Меня зовут Жужа")
