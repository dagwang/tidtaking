import serial.tools.list_ports

def seriallist(printlist = True):
    port_list = serial.tools.list_ports.comports()
    for port in port_list:
        print(port)
    return port_list


if __name__ == "__main__":
    seriallist()