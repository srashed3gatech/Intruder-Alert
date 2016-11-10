import threading

'''This thread is responsible to write frame from frameRepoQ into database'''
class DBFrameWriter(threading.Thread):
    def __init__(self, threadID, name, frameRepoQ):