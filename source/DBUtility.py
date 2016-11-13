from __future__ import print_function
from sqlalchemy import *
from datetime import datetime, timedelta
from classes.RelatedUserInfo import RelatedUserInfo
from classes.VideoFrame import VideoFrame


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
        self.engine.echo = True #to see what sql we are creating
        return self.engine
    
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
        res = ins.execute({'video_path': videoFile, 'duration_sec': -1, 'expiry': videoExpiry.strftime('%Y-%m-%d %H:%M:%S')})
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
#Test Cases: 
if __name__ == "__main__":
    obj = iAlertDB()
    userList = obj.get_realted_users()
    print(userList)

