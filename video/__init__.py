# Don't import PiVideoStream here so we don't crash when importing
# WebcamVideoStream on non-pi systems
# TODO: Hide PiVideoStream and WebCamVideoStream behind VideoStream
from .webcamvideostream import WebcamVideoStream
