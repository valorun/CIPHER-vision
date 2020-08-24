import base64
import time
import json
from threading import Thread, Lock
from .camera import Camera
from .constants import CAMERA_FRAME_RATE
from .object_detection import draw_objects, list_objects

class StreamHandler():
    def __init__(self, client):
        self.client = client
        self.camera = Camera()
        #self.camera.add_processing(draw_objects)
        self.streaming = Lock()

    def _start(self):
        if not self.camera.is_opened():
            self.camera.open()
        self.streaming.acquire()
        self.client.publish('server/started_camera_stream')
        next_frame_time = time.time() + (CAMERA_FRAME_RATE / 60)
        while self.streaming.locked():
            current_time = time.time()
            if next_frame_time <= current_time:
                jpeg = self.camera.get_jpeg_frame()
                jpeg = jpeg.tobytes()
                jpeg = base64.b64encode(jpeg).decode('utf-8')
                self.client.publish('server/camera_stream', 'data:image/jpeg;base64,{}'.format(jpeg))
                next_frame_time = time.time() + (CAMERA_FRAME_RATE / 60)

        self.camera.release()

    def start(self):
        Thread(target=self._start).start()

    def stop(self):
        self.streaming.release()
        self.client.publish('server/stopped_camera_stream')

    def detect_objects(self):
        camera_is_opened = self.camera.is_opened()
        if not camera_is_opened:
            self.camera.open()
        result = list_objects(self.camera.get_frame())
        #result = ','.join(result)
        if not camera_is_opened:
            self.camera.release()
        self.client.publish('server/objects_detected', json.dumps(result))
        