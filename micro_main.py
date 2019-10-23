from Speaker import *
from bluetooth import *
import sys

SERVER = "B8:27:EB:9E:3D:92"

talk("wuuuuf")

client = BluetoothSocket(RFCOMM)
client.connect(SERVER, 3)

box_n = 0

while True:
    sample = get_command()  # получаем строку с командой

    #  обработка ввода номера коробки
    if any([com in sample for com in box_com]):
        for i in range(4):
            if any([com in sample for com in num_coms[i]]):
                box_n = i + 1
                break
        client.send(box_n)
        talk('guv ' * box_n)

    # обработка команды искать
    elif 'forward' in sample:
        talk('вперёд')
        client.send("forward")
        complete = 0
        while not complete:
            client.recv()
            complete = get_confirmation()
            client.send(complete)

        box_n = 0

    # завершение работы
    elif 'stop' in sample:
        talk("Да, конечно, гав гав")
        client.send("stop")
        sys.exit()

    elif 'name' in sample:
        talk("Меня зовут Жужа")
