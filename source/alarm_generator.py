import threading

'''This thread is responsible for:
    - read from frame table and decide candidate alarm frames
    - run algorightm to generate alarms out of those thread
    - purge/clear alarms'''
class BootLoader(threading.Thread):
    def __init__(self, threadID, name, frameRepoQ):