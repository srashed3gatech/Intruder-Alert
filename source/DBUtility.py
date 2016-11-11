from __future__ import print_function
from sqlalchemy import *
from classes.RelatedUserInfo import RelatedUserInfo


''' iAlertDB is all db related functionality provider '''

class iAlertDB:
    
    def __init__(self):
        self.connection_url = "mysql+pymysql://root@localhost/ialertdb"
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
    
          
#Test Cases: 
if __name__ == "__main__":
    obj = iAlertDB()
    userList = obj.get_realted_users()
    print(userList)

