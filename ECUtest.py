import serial
import time
import re

class timer:
    def __init__(self,comport ):
        self.port = serial.Serial(comport, 115200, timeout=5)

    def write_slow(self, command, delay = 0.001):
        for c in command:
            self.port.write(c.encode())
            time.sleep(delay)

    def set_code(self,code):
        if isinstance(code,int):
            code = str(code)
        dummy = self.port.read_all()
        command = '/CD' + code + '\r\n'
        self.write_slow(command)
        output = self.read_line()
        if output[1][1:] == code:
            print('Code ' + code + ' set successfully')
        else:
            print('Code not set, code still ' + output[1][1:])
        return

    def read_line(self):
        raw = self.port.read_until().decode()
        if len(raw) < 4:
            print('No line to read')
            return
        if (raw[0] == '\x02') &  (raw[-3]== '\x03'):
            return re.split('\t',raw[1:-4])
        else:
            print('No line to read')
            return





if __name__ == "__main__":
    ECU = timer('COM10')
    s = ECU.port.read_all()
    print(s)
    ECU.set_code('250')
    s = ECU.port.read_until()
    print(s)
    ECU.port.write('/CD250\r\n'.encode('UTF8'))
    for i in range(20):
        # ECU.set_code(250 + i)
        time.sleep(4)
        s = ECU.read_line()
        print(s)
