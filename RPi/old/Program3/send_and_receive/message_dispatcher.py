import zmq
import json
import time
from threading import Thread

class MessageDispatcher(Thread):
    def __init__(self, data_queue):
        Thread.__init__(self)
        self.ip = "tcp://192.168.0.102:8765"
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.connect()
        self.data_queue = data_queue

    def run(self):
#todo is socket connetec?
        while True:
            try:
                self.publish()
            except (Exception) as e:
                pass

    def publish(self):
        test =self.data_queue.popleft()
        self.socket.send_json(json.dumps(test))
        
    def disconnect(self):
        self.socket.disconnect()

    def connect(self):
        self.socket.bind(self.ip)


