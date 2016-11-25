import numpy as np
import cv2, sys, os, time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import logging
from classes.AlarmFrame import AlarmFrame
from DBUtility import iAlertDB
'''show video by given id and read corresponding frames associated to the alarm and show only the alarmed frames'''

class AlertEmailer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    # return new video file created out of all frames of alarm_frame_obj
    def createTempVideo(self, alarm_frame_obj):
        output_temp_file = os.path.dirname(alarm_frame_obj.video_file)+"/tempalarm_%s_%s_" %(alarm_frame_obj.alarm_category, alarm_frame_obj.alarmid)+time.strftime("%Y%m%d-%H%M%S")+".avi"
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter(output_temp_file,fourcc, 20.0, (320,240))
        cap = cv2.VideoCapture(alarm_frame_obj.video_file)
        cap.set(3 , 640) #width 320
        cap.set(4 , 480) #height 240
        for fameNum in alarm_frame_obj.frame_num:
            cap.set(1, fameNum)
            ret, frame = cap.read()
            out.write(frame)
        cap.release()
            
        return output_temp_file
    # email alarm video file to given email address, then delete the video file
    def emailIAlert(self, video_src_file, emailAddress):
        self.logger.info("Going to send email...")
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
        self.logger.info("Email sent")
        return True
    
if __name__ == "__main__":
    alertEmailerObj = AlertEmailer()
    while True:
        alertEmailerObj.logger.info("Alert Emailer working...")
        #1. read all not sent alarm from db along with their frames
        dbObj = iAlertDB()
        
        alarmFrameObjArr =  dbObj.get_unprocessed_alarm_frames()
        for alarmFrameObj in alarmFrameObjArr:
            #2. generate temp video from frames and video file
            alertEmailerObj.logger.info("Generating alarm video file")
            temp_video_file = alertEmailerObj.createTempVideo(alarmFrameObj)
            
            #3. deliver the video file through email (email got from SYSTEM_USER table)
            alarmReceipients = dbObj.getAlarmReceipients()
            receipientEmails = "ialert6400@gmail.com" #send to myself
            for (userId, email) in alarmReceipients:
                receipientEmails += ","+email
            alertEmailerObj.logger.info("Sending email to %s" %receipientEmails)
            #4. update db indicating alarm processed
            if(alertEmailerObj.emailIAlert(temp_video_file, receipientEmails) == True):
                dbObj.setAlarmProcessed(alarmReceipients, alarmFrameObj.alarmid)
            #5. delete temp video
            alertEmailerObj.logger.info("Deleteing temp alarm video %s" %temp_video_file)
            os.remove(temp_video_file)
        alarmFrameObjArr.logger.info("Alert Emailer going to sleep...")
        time.sleep(30)
    
