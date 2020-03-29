import cv2
from .videostream import VideoStream

class WebcamVideoStream(VideoStream):
    def __init__(self, resolution, hflip=False, vflip=False, src=0):
        """
        initialize the video camera stream and read the first frame
        from the stream
        """
        VideoStream.__init__(self)
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, resolution.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution.height)
        self.hflip = hflip
        self.vflip = vflip

    def get_frame(self):
        _, frame = self.stream.read()
        if self.hflip and self.vflip:
            frame = cv2.flip(frame, -1)
        elif self.hflip:
            frame = cv2.flip(frame, 1)
        elif self.vflip:
            frame = cv2.flip(frame, 0)
        return frame

    def close_stream(self):
        self.stream.release()
