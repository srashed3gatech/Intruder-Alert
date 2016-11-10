import threading

'''This thread is responsible to:
        - write frame to frameRepoQ as it deletect faces from camera feed
        - write video file for recording purpose'''

class CameraCaptureNRecognition(threading.Thread):
    def __init__(self, threadID, name, frameRepoQ):