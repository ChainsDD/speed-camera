from abc import ABCMeta, abstractmethod
from threading import Thread
from future.utils import with_metaclass

class VideoStream(with_metaclass(ABCMeta)):
    def __init__(self):
        self.thread = None
        self.stopped = False
        self.frame = None

    def start(self):
        self.thread = Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.stopped:
                break

            self.frame = self.get_frame()

    def stop(self):
        self.stopped = True
        if self.thread is not None:
            self.thread.join()
        self.close_stream()

    def read(self):
        return self.frame

    @abstractmethod
    def get_frame(self):
        return None

    @abstractmethod
    def close_stream(self):
        pass
