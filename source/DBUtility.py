from sqlalchemy import *

''' iAlertDB is all db related functionality provider '''

class iAlertDB:
    engine = None
    connection_url = None
    
    def __init__(self):
        self.connection_url = "mysql://root@localhost/ialert"
        
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
        
    
    def __del__(self):
        if self.connection is not None:
            self.connection.close()