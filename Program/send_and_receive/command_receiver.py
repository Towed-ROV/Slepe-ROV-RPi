from threading import Thread
import zmq


class CommandReceiver(Thread):
    """ DOCS """

<<<<<<< Updated upstream
    def __init__(self, cmd_queue, host="192.168.0.20", port=8765):
=======
    def __init__(self, cmd_queue, host="192.168.0.223", port=8766):
>>>>>>> Stashed changes
        Thread.__init__(self)
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.REP)
        self.cmd_queue = cmd_queue
        self.host = host
        self.port = port

    def bind(self):
        self.connection.bind("tcp://192.168.0.102:8766")
        print("[STARTED] CommandReceiver")

    def send(self, data):
        self.connection.send_json(data)

    def recv(self):
        return self.connection.recv_json()

    def run(self):
        self.bind()
        while True:
            try:
                cmd = self.recv()
                self.cmd_queue.append(cmd)
            except (Exception) as e:
                pass