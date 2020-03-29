from picamera.array import PiRGBArray # pylint: disable=import-error
from picamera import PiCamera # pylint: disable=import-error

from .videostream import VideoStream

class PiVideoStream(VideoStream):
    def __init__(self, resolution, hflip=False, vflip=False, framerate=30):
        """ initialize the camera and stream """
        VideoStream.__init__(self)
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.hflip = hflip
        self.camera.vflip = vflip
        self.raw_capture = PiRGBArray(self.camera, size=resolution)

    def get_frame(self):
        self.camera.capture(self.raw_capture, format='bgr', use_video_port=True)
        frame = self.raw_capture.array
        self.raw_capture.truncate(0)
        return frame

    def close_stream(self):
        self.raw_capture.close()
        self.camera.close()
