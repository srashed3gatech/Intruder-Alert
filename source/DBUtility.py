from __future__ import print_function
from sqlalchemy import *
from datetime import datetime, timedelta
from classes.RelatedUserInfo import RelatedUserInfo
from classes.VideoFrame import VideoFrame
from classes.VideoFile import VideoFile
from classes.AlarmFrame import AlarmFrame


''' iAlertDB is all db related functionality provider '''

class iAlertDB:
    
    def __init__(self):
        self.connection_url = "mysql+pymysql://root@localhost/ialertdb"
        #self.connection_url = "mysql+pymysql://root@localhost:14924/ialertdb"
        self.engine = None
        
    def _connect_db(self):
        ''' private function - must be called from public functions before db query '''
        if self.engine is not None:
            return self.engine
        self.engine = create_engine(self.connection_url)
        self.engine.echo = False #to see what sql we are creating
        return self.engine
    
    def insert_related_user(self,user):
        db = self._connect_db()
        user_table = Table('USER', MetaData(db), autoload=True)
        insUser = user_table.insert()
        res = insUser.execute({'user_id': user.user_id, 'name' : user.name})
        related_user_table = Table('RELATED_USER', MetaData(db), autoload=True)
        insReUser = related_user_table.insert()
        res = insReUser.execute({'user_id': user.user_id, 'conf_level_thresh':user.conf_level_thresh})
        related_user_pic = Table('RELATED_USER_PICTURE', MetaData(db), autoload=True)
        insReUserPic = related_user_pic.insert()
        res = insReUserPic.execute({'user_id': user.user_id,'pic_id': user.pic_id, 'pic_path': user.pic_path})
    
    def get_realted_users(self):
        '''return array of object RelatedUser existing in db'''
        relatedUsersList = []
        db = self._connect_db()
        viewRealtedUser = Table('recog_users', MetaData(db), autoload=True)
        stmt = viewRealtedUser.select()
        rs = stmt.execute()
        for row in rs:
            relatedUserInfo = RelatedUserInfo(row[viewRealtedUser.c.user_id], row[viewRealtedUser.c.pic_id], 
                                              row[viewRealtedUser.c.pic_path], row[viewRealtedUser.c.conf_level_thresh])
            relatedUsersList.append(relatedUserInfo)
        return relatedUsersList
    
    def create_new_video_file(self, videoFile): #returns a videoObj tuple
        db = self._connect_db()
        videoTable = Table('VIDEO', MetaData(db), autoload=True)
        ins = videoTable.insert()
        videoExpiry = datetime.now()+timedelta(hours=3) #video expire after 3 hours
        res = ins.execute({'video_path': videoFile, 'duration_sec': -1, 'framerate': 20, 'expiry': videoExpiry.strftime('%Y-%m-%d %H:%M:%S')})
        return {"video_id": res.lastrowid,  
                "video_path": videoFile, 
                "duration_sec": -1, 
                "expiry": videoExpiry.strftime('%Y-%m-%d %H:%M:%S')}
    
    def insert_frames(self, vFrames):
        if(len(vFrames) == 0):
            return
        framesDictArr = [] #array of dict
        corrspToArr = [] #array of dict
        
        for frameObj in vFrames:
            framesDictArr.append({'video_id': frameObj.video_id,
                                  'frame_num': frameObj.frame_num, 
                                  'timestamp': frameObj.timestamp})
            if(frameObj.user_id != -1): #its a know user frame, an entry in corresponds_to table
                corrspToArr.append({'user_id': frameObj.user_id,
                                    'video_id': frameObj.video_id,
                                    'frame_num': frameObj.frame_num,
                                    'conf_level': frameObj.confid_level,
                                    'face_num': 0 }) #TODO: face_num value not curently coming from cam capture
                 
        db = self._connect_db()
        frameTable = Table('FRAME', MetaData(db), autoload=True)
        insFrame = frameTable.insert()
        insFrame.execute(framesDictArr);
        
        if(len(corrspToArr) > 0):
            corresponds_toTable = Table('CORRESPONDS_TO', MetaData(db), autoload=True)
            instCT = corresponds_toTable.insert()
            instCT.execute(corrspToArr)
    
    def get_video_file(self, video_id): #returns a videoObj tuple
        db = self._connect_db()
        videoTable = Table('VIDEO', MetaData(db), autoload=True)
        sel = videoTable.select(videoTable.c.video_id == video_id)
        res = sel.execute();
        for row in res: #just single record in case we have something with given id
            videoFileObj = VideoFile(row[videoTable.c.video_id], row[videoTable.c.time_created],
                                 row[videoTable.c.duration_sec], row[videoTable.c.video_path],
                                 row[videoTable.c.framerate], row[videoTable.c.expiry])
        return videoFileObj
    
    def get_unprocessed_alarm_frames(self): #send alarms that not been sent and not cleared
        #this should be a view
        db = self._connect_db()
        openAlarmTable = Table('unprocessed_open_alarm', MetaData(db), autoload=True)
        uniqueAlarmIdsSel = select([distinct(openAlarmTable.c.alarm_id)])
        retAlarmFrameArr = []
        for alarmId in uniqueAlarmIdsSel.execute():
            selAllAlarmFrameAttr = select([openAlarmTable.c.alarm_id, openAlarmTable.c.cate_name,
                 openAlarmTable.c.first_occ, openAlarmTable.c.last_occ, 
                 openAlarmTable.c.tally, openAlarmTable.c.clear_time,
                 openAlarmTable.c.video_id, openAlarmTable.c.video_path], openAlarmTable.c.alarm_id == alarmId[openAlarmTable.c.alarm_id]).limit(1)
            results = selAllAlarmFrameAttr.execute()
            if results.rowcount == 0:
                continue
            for result in results:
                alarmFrameObj = AlarmFrame(result[openAlarmTable.c.alarm_id],
                                       result[openAlarmTable.c.cate_name], 
                                       result[openAlarmTable.c.first_occ],
                                       result[openAlarmTable.c.last_occ],
                                       result[openAlarmTable.c.tally],
                                       result[openAlarmTable.c.clear_time],
                                       result[openAlarmTable.c.video_id],
                                       result[openAlarmTable.c.video_path], 
                                       [])
                
                selAlarmFrames = select([openAlarmTable.c.frame_num], openAlarmTable.c.alarm_id == alarmId[openAlarmTable.c.alarm_id])
                resultFrames = selAlarmFrames.execute()
                for frame in resultFrames:
                    alarmFrameObj.frame_num.append(frame[openAlarmTable.c.frame_num])
                
                retAlarmFrameArr.append(alarmFrameObj)
        
        return retAlarmFrameArr
    
    def getAlarmReceipients(self):
        #send userid and email from SYSTEM_USER table
        db = self._connect_db()
        user_table = Table('SYSTEM_USER', MetaData(db), autoload=True)
        stmt = user_table.select()
        rs = stmt.execute()
        receipients = []
        for row in rs:
            receipients.append((row[user_table.c.user_id], row[user_table.c.email]))
        
        return receipients
        
    def setAlarmProcessed(self, alarmReceipients, alarmId):
        #write SENT_TO table as 1 for alarm and receipients userid) 
        db = self._connect_db()
        sendToTable = Table('SENT_TO', MetaData(db), autoload=True)
        sendToDictArr = []
        for (user_id, email) in alarmReceipients:
            sendToDictArr.append({"user_id": user_id,
                                  "alarm_id": alarmId,
                                  "status": 1})
        insSendTo = sendToTable.insert()
        insSendTo.execute(sendToDictArr); 
    
    
#Test Cases: 
if __name__ == "__main__":
    obj = iAlertDB()
    '''u = RelatedUserInfo(1,1,"test",100)
    obj.insert_related_user(u)
    userList = obj.get_realted_users()
    print(userList)'''
    '''videoFileObj = obj.get_video_file(101)
    print(videoFileObj)'''
    obj.get_unprocessed_alarm_frames()

