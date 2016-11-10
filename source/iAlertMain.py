import threading

''' Main entry point for the program 
    1. start bootloader thread and make other wait, once its done join() it
        - load realated user using db utility
        - train system using images for user-id's image path and generate face_recognizer.xml
        - generate new video file and update database with video file info
        
    2. start camcapture thread - pass facerecognizer.xml and new video file path
    
    3. start db_framewriter thread
    
    NEXT...TODO
    4. start alarm generator thread
'''
faceRecogXmlFilePath = None
videoFilePath = None

