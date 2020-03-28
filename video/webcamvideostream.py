from threading import Thread
import cv2

class WebcamVideoStream:
    def __init__(self, src, width, height, hflip, vflip):
        """
        initialize the video camera stream and read the first frame
        from the stream
        """
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.hflip = hflip
        self.vflip = vflip
        (self.grabbed, self.frame) = self.stream.read()
        self.thread = None
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        """ start the thread to read frames from the video stream """
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        """ keep looping infinitely until the thread is stopped """
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.stream.release()
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            #check for valid frames
            if not self.grabbed:
                # no frames recieved, then safely exit
                self.stopped = True
        self.stream.release()    #release resources

    def read(self):
        """ return the frame most recently read
            Note there will be a significant performance hit to
            flip the webcam image so it is advised to just
            physically flip the camera and avoid
            setting WEBCAM_HFLIP = True or WEBCAM_VFLIP = True
        """
        if (self.hflip and self.vflip):
            self.frame = cv2.flip(self.frame, -1)
        elif self.hflip:
            self.frame = cv2.flip(self.frame, 1)
        elif self.vflip:
            self.frame = cv2.flip(self.frame, 0)
        return self.frame

    def stop(self):
        """ indicate that the thread should be stopped """
        self.stopped = True
        # wait until stream resources are released (producer thread might be still grabbing frame)
        if self.thread is not None:
            self.thread.join()  # properly handle thread exit

    def isOpened(self):
        return self.stream.isOpened()
