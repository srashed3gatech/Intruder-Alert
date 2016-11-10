from sqlalchemy import *
from classes.RelatedUserInfo import RelatedUserInfo

''' iAlertDB is all db related functionality provider '''

class iAlertDB:
    
    def __init__(self):
        self.connection_url = "mysql+pymysql://root@localhost:14924/ialertdb"
        self.connection_url = None
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
        db = self._connect_db()
        allKnownUsers = Table('recog_users', MetaData(db), autoload=True)
        stmt = allKnownUsers.select()
        rs = stmt.execute()
        for row in rs:
            '''relatedUserInfo = RelatedUserInfo()
            relatedUserInfo.user_id = row[allKnownUsers.c.user_id]
            relatedUserInfo.pic_id = row[allKnownUsers.c.pic_id]
            relatedUserInfo.pic_path = row[allKnownUsers.c.pic_path]
            relatedUserInfo.conf_level_thresh = row[allKnownUsers.c.conf_level_thresh]
            relatedUserInfoList.append(relatedUserInfo)'''
            print row
    
    def __del__(self):
        if self.engine is not None:
            #do nothing - handled by sqlalchemy
            self.engine = None
            return
          
#Test Cases:   
obj = iAlertDB()
obj.get_realted_users()