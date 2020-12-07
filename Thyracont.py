class VD85:
    #  Thyracont VD85 pressure gauge \
    #  Documentation https: // thyracont - vacuum.com /?ddownload = 16602
    #  Driver:  https: // thyracont - vacuum.com /?ddownload = 16531
    def __init__(self,comport=None):
        import time
        import serial
        import serial.tools.list_ports
        if comport == None:
            comlist = serial.tools.list_ports.comports()
            connected = []
            self.portname = '' # Member variable char/string # Comments are Tarjeis for MOOG2
            self.ser = [] # Member variable list
            for element in comlist:
                connected.append(element.device) # Connected is a list of serial.tools.list_ports.device str values
            print('Available ports: ' + str(connected)) # Prints available ports to display
            cmdbytes = b'000T' # Creates bytestring, what does this specific values mean?
            cks = divmod(sum(cmdbytes) , 64)[1] + 64 # Checksum defined as sum over bytes from fields address, code and data mod 64 + 64
            cmd = cmdbytes + chr(cks).encode() + '\r'.encode() # Creates entire command bytestring for type-query
            for portname in connected: # Iterates through available com-ports
                with serial.Serial(portname, 9600, timeout=5) as ser:
                    ser.write(cmd)
                    time.sleep(0.1)
                    answer = ser.read_all()
                    #print(portname, answer)
                    if str(answer).find('V8U005') > 0: # Checks if VD85 is connected to that port
                        self.portname = portname
                    ser.close()
            print('VD85 Choosing: ' + self.portname)
        else: # If only one available com-port, that is VD85
            self.portname = comport
        time.sleep(0.1)
        self.ser = serial.Serial(self.portname, 9600, timeout=5)

    def write_read(self,cmd):
        import time
        cmdbytes = ('000' + cmd).encode()
        cks = divmod(sum(cmdbytes),64)[1] + 64
        cmd = cmdbytes + chr(cks).encode() + '\r'.encode()
        time.sleep(0.05)
        self.ser.write(cmd)
        time.sleep(0.1)
        out = self.ser.read_all()
        return out

    def p(self): # Function for calculating pressure in mbar
        answer = self.write_read('M')
        while len(answer) != 12:
            answer = self.write_read('M')
        number = int(answer[4:8].decode())
        exponent = int(answer[8:10].decode())-23
        return(number*10**(exponent))

    def __del__(self):
        toclose = self.ser
        toclose.close()
        #self.ser.close()
