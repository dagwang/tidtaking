import serial
import serial.tools.list_ports
import time
import datetime
import re
#from PyQt5 import QtCore
# Class for EMIT tag readers (ETS, ECU, ECB)
# Documentation: https://www.emit.no/wp-content/uploads/2020/06/pc-protocol_1.1.pdf


class TagReader():
    def __init__(self, comport):
        super().__init__()
        self.port = serial.Serial(comport, 115200, timeout=5)

    def write_slow(self, command, delay = 0.005):
        for c in command:
            self.port.write(c.encode())
            time.sleep(delay)

    def set_code(self, code):
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
        if (raw[0] == '\x02') & (raw[-3]== '\x03'):
            return re.split('\t', raw[1:-4])
        else:
            print('No line to read')
            return

    def read_line_when_available(self):
        while self.port.in_waiting < 10:
            time.sleep(0.3)
            #print(self.port.in_waiting)
        time.sleep(0.05)
        return self.read_line()

    def read_tag_when_available(self):
        while 1:
            lastline = self.split_message(self.read_line_when_available())
            if 'tag' in lastline:
                return lastline

    def split_message(self, message):
        status = dict()
        for entry in message:
            if entry[0] == 'Y':
                status.update(dict(serial=entry[1:]))
            elif entry[0] == 'C':
                status.update(dict(code=entry[1:]))
            elif entry[0] == 'O':
                status.update(dict(retries=entry[1:]))
            elif entry[0] == 'B':
                status.update(dict(message_type=entry[1:]))
            elif entry[0] == 'X':
                status.update(dict(mode=entry[1:]))
            elif entry[0] == 'I':
                status.update(dict(type=entry[1:4]))
            elif entry[0] == 'W':
                tid = datetime.time.fromisoformat(entry[1:])
                status.update(dict(status_time=tid))
            elif entry[0] == 'T':
                tid = datetime.time.fromisoformat(entry[1:])
                status.update(dict(tag_time=tid))
            elif entry[0] == 'E':
                tid = datetime.time.fromisoformat(entry[1:])
                status.update(dict(read_time=tid))
            elif entry[0] == 'N':
                status.update(dict(tag=entry[1:]))

        return status

    def get_status(self):
        command = '/ST\r\n'
        self.write_slow(command)
        message = self.read_line()
        status = self.split_message(message)
        return status


class ReaderManager:
    def __init__(self):
        port_list = serial.tools.list_ports.comports()
        unit_list = []
        for port in port_list:
            try:
                reader = TagReader(port.device)
                status = reader.get_status()
                if status['type'] in ['ECU','ETS','ECB']:
                    status.update(dict(port=port))
                    unit_list.append(status)
                del reader
            except:
                continue
        self.port_list = port_list
        self.unit_list = unit_list

    def connect_first(self):
        reader = TagReader(self.unit_list[0]['port'].device)
        return reader

if __name__ == "__main__":
    m = ReaderManager()
    ECU = m.connect_first()
    s = ECU.get_status()
    print(s)
    ECU.set_code('70')
    s = ECU.read_line_when_available()
    print(s)
    print(ECU.split_message(s))
    ECU.port.write('/CD250\r\n'.encode('UTF8'))
    for i in range(20):
        # ECU.set_code(250 + i)
        s = ECU.read_tag_when_available()
        print(s)

