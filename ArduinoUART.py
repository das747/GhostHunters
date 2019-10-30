import serial
from time import sleep

COMMANDS = {'forwards': 5, 'return': 6}


class PySerial(serial.Serial):
    def __init__(self, port, baud_rate=9600):
        try:
            super().__init__(port, baud_rate)
        except serial.serialutil.SerialException:
            while True:
                print("Arduino not connected!")
                sleep(1)

    def write_int(self, val):
        self.write(int.to_bytes(val, 1, 'big'))

    def read_int(self, *args):
        received = self.read(*args)
        return int.from_bytes(received, 'big')

    def write_command(self, command):
        self.write_int(COMMANDS[command])


if __name__ == '__main__':
    port = '/dev/ttyUSB0'
    ser = PySerial(port)
    while 1:
        ser.write_int(int(input()))
        while not ser.in_waiting:
            pass
        while ser.in_waiting:
            print(ser.read_int())
