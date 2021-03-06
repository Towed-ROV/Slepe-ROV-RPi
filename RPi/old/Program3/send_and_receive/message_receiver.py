import json
import zmq
from threading import Thread
class MessageReceiver(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.ip = "tcp://192.168.0.20:8765"
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(self.ip)
        self.socket.subscribe('')
        self.queue = queue
    def run(self):
        while True:
            try:
                self.subscribe()
            except zmq.ZMQError:
                print("could not receive data")

    def subscribe(self):
        received_data = json.loads(self.socket.recv_json())
        self.queue.append(received_data)
        test = self.queue.popleft()
        print(test)
        self.queue.append(test)

    def connect(self):
        self.socket.connect(self.ip)

    def disconnect(self):
        self.socket.disconnect()









