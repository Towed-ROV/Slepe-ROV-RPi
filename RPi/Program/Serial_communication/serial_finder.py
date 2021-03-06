import glob
import serial
import sys
from time import sleep 


class SerialFinder:
    """
    Finding all available serial ports and check each if they are the correct one and returns a list of these.
    """
    def __init__(self):
        self.port_name_list = {}
        self.seperation_char = ':'
        self.baud_rate = 0

    def find_com_ports(self):
        """
        Loop through all available com ports on rpi and multiple baud rates.
        :return: dict with all found com ports
        """
        search_runs = 0
        port_names = self.get_available_com_ports()
        print(port_names)
        while search_runs != 2:
            if search_runs == 0:
                self.baud_rate = 57600
            if search_runs == 1:
                self.baud_rate = 115200

            for key in port_names:
                # if 'dev' in key:
                serial_port = serial.Serial(key, self.baud_rate, timeout=1,
                                            stopbits=1, bytesize=8)
                serial_port.write("<reset:True>".encode('utf-8'))
                print(key)
                print(self.baud_rate)
                try:
                    sleep(2)
                    if serial_port.in_waiting:
                        message_received = serial_port.readline()
                        if message_received:
                            print(message_received,'stig')
                            message_received = message_received.strip().decode('utf-8').split(self.seperation_char)
#                             print(message_received,'kato')
                            port_name = message_received[0].replace('<', '')
                            if 'IMU' in port_name and self.baud_rate == 57600:
                                self.port_name_list[key] = 'IMU'
                                print('Found IMU')

                            elif 'SensorArduino' in port_name:
                                self.port_name_list[key] = 'SensorArduino'
                                print('Found SensorArduino')
                                print(self.baud_rate)

                            elif 'StepperArduino' in port_name:
                                self.port_name_list[key] = 'StepperArduino'
                                print('Found StepperArduino')
                        serial_port.reset_input_buffer()
                        serial_port.close()
                except (Exception) as e:

                    print(e, 'serial finder')

                    try:
                        serial_port.close()
                    except (Exception) as e:
                        print(e, 'serial finder')
            search_runs = search_runs + 1
        print('done')
        return self.port_name_list

    def get_available_com_ports(self):
        """
        find all available com port on Windows or linux systems
        :return: dict with all com ports
        """

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result






