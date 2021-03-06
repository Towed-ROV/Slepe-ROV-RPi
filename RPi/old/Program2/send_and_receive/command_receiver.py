from threading import Thread
import zmq


class CommandReceiver(Thread):
    """ DOCS """

    def __init__(self, cmd_queue, host="10.0.0.27", port=8767):
        Thread.__init__(self)
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.REP)
        self.cmd_queue = cmd_queue
        self.host = host
        self.port = port

    def bind(self):
        self.connection.bind("tcp://10.0.0.27:8767")
        print("[STARTED] CommandReceiver")
        

    def send(self, data):
        self.connection.send_json(data)

    def recv(self):
        test =  self.connection.recv_json()
        print(test, "command recv")
        return test

    def run(self):
        self.bind()
        while True:
            try:
                cmd = self.recv()
                self.cmd_queue.put(cmd)
                self.send({"success" : True})
            except (Exception) as e:
                print(e, 'command_receiver')