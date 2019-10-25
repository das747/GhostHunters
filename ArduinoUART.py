import serial
from time import sleep

COMMANDS = {'forwards': 5, 'return': 6}  # словарь команд для метода write_command


# более удобный класс Serial из пакета pyserial
class PySerial(serial.Serial):
    def __init__(self, port, baud_rate=9600):
        try:
            super().__init__(port, baud_rate)
        # обработка ошибки подключения, чаще всего неправильно указан порт
        except serial.serialutil.SerialException:
            while True:
                print("Arduino not connected!")
                sleep(1)

    # упрощённая передача целого числа
    def write_int(self, val):
        self.write(int.to_bytes(val, 1, 'big'))

    # упрощённое считывание целого числа
    def read_int(self, *args):
        received = self.read(*args)
        return int.from_bytes(received, 'big')

    # ввод команды через словарь
    def write_command(self, command):
        self.write_int(COMMANDS[command])


# код для тестов
if __name__ == '__main__':
    port = '/dev/ttyUSB0'  # можно проверить через ArduinoIDE
    ser = PySerial(port)
    # считываем число и пишем в ардуину, печатаем ответ
    while 1:
        ser.write_int(int(input()))
        while not ser.inWaiting:  # ожидание входящих данных
            pass
        print(ser.read_int())
