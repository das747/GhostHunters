from Speaker import *
from bluetooth import *
import argparse
import sys

addr_dict = {'pi5': 'B8:27:EB:9E:3D:92', 'red': 'B8:27:EB:AE:01:FF', 'micro': 'B8:27:EB:4A:F7:21'}

talk("wuuuuf")

ap = argparse.ArgumentParser()
ap.add_argument('-r', "--recognizer", type=str, default='sphinx',
                help="recognizer type, google or sphinx")
ap.add_argument("-n", "--name", type=str, default="pi5",
                help="chose server name")
args = vars(ap.parse_args())

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
        client.send(str(box_n))
        client.send('forward')
        talk('guv ' * box_n)

    # обработка команды искать
    elif ' go' in sample:
        client.send("forward")
        talk('вперёд')
        complete = 0
#         while not complete:
#             client.recv(16)
#             complete = get_confirmation()
#             client.send(complete)

        box_n = 0

    # завершение работы
    elif 'stop' in sample:
        client.send("stop")
        talk("Да, конечно, гав гав")
        sys.exit()

    elif 'name' in sample:
        talk("Меня зовут Жужа")
