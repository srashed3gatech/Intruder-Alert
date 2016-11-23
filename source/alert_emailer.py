import numpy as np
import cv2
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import threading
import time
import logging
'''show video by given id and read corresponding frames associated to the alarm and show only the alarmed frames'''

class AlertEmailer(threading.Thread):
    def __init__(self, timeout):
        self.timeout = timeout
    
    def run(self):
        self.logger.info("Alert Emailer working...")
        #1. read all not sent alarm from db along with their frames
        #2. generate temp video from frames and video file
        #3. deliver the video file through email (email got from SYSTEM_USER table)
        #4. delete temp video
        #5. go to sleep for timeout time
        self.logger.info("Alert Emailer going to sleep...")
    # return new video file created out of all frames of alarm_frame_obj
    def createTempVideo(video_src_file, alarm_frame_obj):
        cap = cv2.VideoCapture(video_src_file)
        cap.set(3 , 320) #width 320
        cap.set(4 , 240) #height 240
        while(cap.isOpened()):
            ret, frame = cap.read()
            
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
    
    # email alarm video file to given email address, then delete the video file
    def emailIAlert(video_src_file, emailAddress):
        fromaddr = "ialert6400@gmail.com"
        toaddr = emailAddress
        
        msg = MIMEMultipart()
        
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "!!Intruder!!"
        
        body = "iAlert detected intruder on monitored premise... please check attached video for detail"
        
        msg.attach(MIMEText(body, 'plain'))
        
        filename = "alarmvideo.avi"
        attachment = open(video_src_file, 'rb')
        
        part = MIMEBase('application', 'octate-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= %s' %filename)
        
        msg.attach(part)
        
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(fromaddr, '1234567890;')
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    
if __name__ == "__main__":
    #writeTempVideo("sample.avi", alarm_frames)
    emailIAlert("../Video/cam_cap_20161120-191532.avi","srashed3gatech@gmail.com")
