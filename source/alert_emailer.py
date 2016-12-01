import numpy as np
import cv2, sys, os, time
from PIL import Image
import smtplib
import threading
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import logging
from classes.AlarmFrame import AlarmFrame
from DBUtility import iAlertDB
'''show video by given id and read corresponding frames associated to the alarm and show only the alarmed frames'''

class AlertEmailer(threading.Thread):
    def __init__(self, threadID, name, exitThreadFlag, dbConn, sleepTime):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.threadID = threadID
        self.exitThreadFlag = exitThreadFlag
        self.dbConn = dbConn
        self.sleepTime = sleepTime
    
    def run(self):
        while True:
            self.logger.info("Alert Emailer working...")
            try:
                alarmFrameObjArr =  self.dbConn.get_unprocessed_alarm_frames()
                for alarmFrameObj in alarmFrameObjArr:
                    #2. generate temp video from frames and video file
                    self.logger.info("Generating alarm video file")
                    temp_video_file = self.createTempVideo(alarmFrameObj)
                    
                    #3. deliver the video file through email (email got from SYSTEM_USER table)
                    alarmReceipients = self.dbConn.getAlarmReceipients()
                    receipientEmails = "ialert6400@gmail.com" #send to myself
                    for (userId, email) in alarmReceipients:
                        receipientEmails += ", "+email
                    self.logger.info("Sending email to %s" %receipientEmails)
                    #4. update db indicating alarm processed
                    if(self.emailIAlert(temp_video_file, receipientEmails) == True):
                        self.dbConn.setAlarmProcessed(alarmReceipients, alarmFrameObj.alarmid)
                    
            except Exception as e: 
                self.logger.warning("Alert Emailer exception: %s" %e)
            finally:
                self.logger.info("Alert Emailer going to sleep...")
                time.sleep(self.sleepTime)
                if self.exitThreadFlag:
                   break;
        self.logger.info("Alert Emailer Stopped!")
    # return new video file created out of all frames of alarm_frame_obj
    def createTempVideo(self, alarm_frame_obj):
        if(os.path.isfile(alarm_frame_obj.video_file)):
            print "%s - size: %s" %(alarm_frame_obj.video_file, os.path.getsize(alarm_frame_obj.video_file)) 
        else:
            raise IOError("File not found: %s" %alarm_frame_obj.video_file)
        
        cap = cv2.VideoCapture(alarm_frame_obj.video_file)
        if(not cap.isOpened()):
            return -1;
        
        cap.set(3 , 640) #width 320
        cap.set(4 , 480) #height 240
        
        output_temp_file = os.path.dirname(alarm_frame_obj.video_file)+"/tempalarm_%s_%s_" %(alarm_frame_obj.alarm_category, alarm_frame_obj.alarmid)+time.strftime("%Y%m%d-%H%M%S")+".avi"
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter(output_temp_file,fourcc, 20.0, (640, 480))
        
        for fameNum in alarm_frame_obj.frame_num:
            cap.set(1 , fameNum)
            ret, frame = cap.read()
            #frame = imutils.resize(frame, width=400)
            #print "Width: %s, Height:%s" %(cap.get(3), cap.get(4))
            try:
                out.write(frame)
            except Exception as e:
                self.logger.warning("Alert Emailer Create Video exception: %s" %e)
                pass
        cap.release()
        out.release()
            
        return output_temp_file
    # email alarm video file to given email address, then delete the video file
    def emailIAlert(self, video_src_file, emailAddress):
        self.logger.info("Going to send email...")
        fromaddr = "ialert6400@gmail.com"
        toaddr = emailAddress
        video_delete_flag= True
        msg = MIMEMultipart()
        
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "!!Intruder!!"
        
        body = "iAlert detected intruder on monitored premise... please check attached video for detail"
        
        if os.path.getsize(video_src_file) < 20000000 :
            filename = "alarmvideo.avi"
            attachment = open(video_src_file, 'rb')
        
            part = MIMEBase('application', 'octate-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename= %s' %filename)
            
            msg.attach(part)
            attachment.close()
        else:
            body = "iAlert detected intruder on monitored premise... \n but Alarm video discarded due to huge size (you can still check the file at server: %s)" %video_src_file
            video_delete_flag = False
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(fromaddr, '1234567890;')
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        self.logger.info("Email sent")
        
        #5. delete temp video
        if video_delete_flag: 
            self.logger.info("Deleteing temp alarm video %s" %video_src_file)
            os.remove(video_src_file)
        return True
    
if __name__ == "__main__":
    logging.basicConfig()
    alertEmailerObj = AlertEmailer(1, "alert-emailer", False, iAlertDB(), 10)
    #alertEmailerObj.start()
    #while True:
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
            receipientEmails += ", "+email
        alertEmailerObj.logger.info("Sending email to %s" %receipientEmails)
        #4. update db indicating alarm processed
        if(alertEmailerObj.emailIAlert(temp_video_file, receipientEmails) == True):
            dbObj.setAlarmProcessed(alarmReceipients, alarmFrameObj.alarmid)
    alertEmailerObj.logger.info("Alert Emailer going to sleep...")
    time.sleep(30)
    
    
