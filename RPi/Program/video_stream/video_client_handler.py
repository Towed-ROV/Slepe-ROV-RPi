from video_camera import VideoCamera
from threading import Thread
from util import process_frame



class VideoClientHandler(Thread):
    def __init__(self, client_connection, client_info):
        Thread.__init__(self)
        self.client_connection = client_connection
        self.client_info = client_info
        self.streaming_flag = None
        self.client_socket = None
        self.camera = None
        self.log = None

    def add_logger(self, log):
        self.log = log

    def add_streaming_flag(self, streaming_flag):
        self.streaming_flag = streaming_flag

    def run(self):
        if not self.streaming_flag:
            raise Exception("Missing stream flag")
        if not self.log:
            raise Exception("Missing logger")
        if not self.camera:
            self.camera = VideoCamera()
        try:
            while self.streaming_flag.is_set():
                frame_bytes = self.camera.get_frame_bytes()
                payload = process_frame(frame_bytes)
                self.client_connection.sendall(payload)
            self.client_connection.close()
        except ConnectionAbortedError:
            self.log.error(f"ConnectionAbortedError : {self.client_info}")
        except ConnectionResetError:
            self.log.error(f"ConnectionResetError   : {self.client_info}")
        finally:
            self.log.warning(f"VideoClientHandler exit: {self.client_info}")
            self.camera.close()
            self.camera = None  
            
