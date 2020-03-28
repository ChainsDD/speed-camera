from threading import Thread
# pylint: disable=import-error
from picamera.array import PiRGBArray
from picamera import PiCamera
# pylint: enable=import-error

class PiVideoStream:
    def __init__(self, resolution, framerate, rotation, hflip, vflip):
        """ initialize the camera and stream """
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.rotation = rotation
        self.camera.framerate = framerate
        self.camera.hflip = hflip
        self.camera.vflip = vflip
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.raw_capture,
                                                     format="bgr",
                                                     use_video_port=True)

        """
        initialize the frame and the variable used to indicate
        if the thread should be stopped
        """
        self.thread = None
        self.frame = None
        self.stopped = False

    def start(self):
        """ start the thread to read frames from the video stream """
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        """ keep looping infinitely until the thread is stopped """
        for frame in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = frame.array
            self.raw_capture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.raw_capture.close()
                self.camera.close()
                return

    def read(self):
        """ return the frame most recently read """
        return self.frame

    def stop(self):
        """ indicate that the thread should be stopped """
        self.stopped = True
        if self.thread is not None:
            self.thread.join()
