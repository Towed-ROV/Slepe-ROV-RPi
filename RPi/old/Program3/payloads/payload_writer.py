import json
import time
from send_and_receive.message_dispatcher import MessageDispatcher
from threading import Thread
from collections import deque
class PayloadWriter(Thread):
    def __init__(self, sensor_list):
        Thread.__init__(self)
        self.sensor_list = sensor_list
        self.message_queue = deque()
        self.message_dispatcher = MessageDispatcher(self.message_queue)
        self.message_dispatcher.daemon = True
        self.message_dispatcher.start()


    def run(self):
        time.sleep(10)
        while True:
            try:
                self.__merge_sensor_payload()
            except (Exception) as e:
                print(e,"payload writer")

    def merge_command_payload(self, command):
        command_structure = {
            "payload_name": "command",
            "payload_data": [command]
        }
        

    def __merge_sensor_payload(self):
        sensors = []
        json_sensor = ''
        
#         for sensor_name, sensor_value in self.sensor_list.items():
            
#             sensors.append('%s:%s'%sensor_name, sensor_value)
        json_sensor = json.dumps(self.sensor_list)
        time.sleep(0.05)
        sensor_structure = {
            "payload_name": "sensor_data",
            "payload_data": json_sensor
        }
        
#         print('-----------')
#         print(sensor_structure)
#         print('-----------')

        self.message_queue.append(sensor_structure)

if __name__ == "__main__":
    sensor_list = {}
    sensor_list["test"] = 10
    sensor_list["test2"] = 123
    sensor_list["kr[re"] = 1231231
    payload = PayloadWriter()
    test = payload.merge_payload(sensor_list)

