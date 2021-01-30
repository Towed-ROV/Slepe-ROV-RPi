import serial
import time
from threading import Thread
class SerialReader(Thread):
    def __init__(self, com_port, baud_rate):
        Thread.__init__(self)
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.serial(self.com_port, self.baud_rate, timeout=0)

    def run(self):
        while True:
            try:
                self.read_incomming_data()
            except (Exception)as e:
                print(e)

    def read_incomming_data(self):
        start_char = '<'
        end_char = '>'
        seperation_char = ':'
        message_received = ""

        if(not self.serial_port.is_open):
            try:
                self.serial_port.open()
            except(Exception) as e:
                print(e)
        while True:
            time.sleep(0.05)
            message_received = self.serial_port.readline()
            message_received = message_received.strip()
            if message_received:
                message_received = message_received.decode().strip(start_char).strip(end_char).split(seperation_char)
                break
        return message_received








