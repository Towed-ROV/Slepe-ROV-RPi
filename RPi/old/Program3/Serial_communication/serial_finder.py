import glob
import serial
import time


class SerialFinder:
    def __init__(self):
        self.port_name_list = {}
        self.seperation_char = ":"
        self.baud_rate = 0

    def find_com_ports(self):
        search_runs = 0
        port_names = self.get_available_com_ports()
        print(port_names)
        while search_runs != 4:
            if search_runs == 0:
                self.baud_rate = 4800
            if search_runs == 1:
                self.baud_rate = 9600
            if search_runs == 2:
                self.baud_rate = 57600
            if search_runs == 3:
                self.baud_rate = 115200

            for key in port_names:
                if 'dev' in key:
                    serial_port = serial.Serial(key, self.baud_rate, timeout=0,
                                                stopbits=1, bytesize=8)
                    try:
                        time.sleep(2)
                        message_received = serial_port.readline()
                        print(message_received)
                        if message_received:
                            message_received = message_received.strip().decode().split(self.seperation_char)
                            port_name = message_received[0].replace('<', '')
                            if "IMU" in port_name:
                                self.port_name_list[key] = "IMU"
                                print('Found IMU')

                            elif "sensorArduino" in port_name:
                                self.port_name_list[key] = "SensorArduino"
                                print('Found SensorArduino')

                            elif "stepperArduino" in port_name:
                                self.port_name_list[key] = "StepperArduino"
                                print('Found StepperArduino')
                        serial_port.close()
                    except (Exception) as e:
                        print(e, "serial finder")
                        try:
                            serial_port.close()
                        except (Exception) as e:
                            print(e, "serial finder")
            search_runs = search_runs + 1
        print("done")
        return self.port_name_list

    def get_available_com_ports(self):
        ports = glob.glob('/dev/tty[A-Za-z]*')
        port_names = []
        port_exceptions = ['dev/ttyprintk']
        i = 0
        while i < 3:
            for port in port_exceptions:
                if port in ports:
                    print("seff")
                    ports.remove(port)
            for port in ports:
                try:
                    s = serial.Serial(port, self.baud_rate, timeout=0)
                    port_names.append(port)
                except (OSError, serial.SerialException):
                    pass
                time.sleep(0.2)
            i = i + 1
        if not port_names:
            print("There are no serial-ports available")
        port_names = list(dict.fromkeys(port_names))
        return list(port_names)





