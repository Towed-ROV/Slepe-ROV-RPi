import zmq
import json
from threading import Thread

class MessageDispatcher(Thread):
    def __init__(self, data_queue):
        Thread.__init__()
        self.ip = "tcp://192.168.0.20:1337"
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(self.ip)
        self.data_queue = data_queue

    def run(self):
        while True:
            try:
                self.publish()
            except (Exception) as e:
                print(e)

    def publish(self):
        self.socket.send_json(json.dumps(self.data_queue.popleft()))

    def disconnect(self):
        self.socket.disconnect()

    def connect(self):
        self.socket.bind(self.ip)

