import threading

'''This thread is responsible for:
    - read all related users from DBUtitity.get_realted_users
    - train and generate face_recognizer.xml at startup'''
class BootLoader(threading.Thread):
    def __init__(self, threadID, name, frameRepoQ):