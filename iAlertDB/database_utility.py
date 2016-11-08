from sqlalchemy import *


class iAlertDB:
    engine = None
    
    def __init__(self):
        return;
        
    def connect_db(self):
        if self.engine is not None:
            return self.engine
        self.engine = create_engine("mysql://root@localhost/ialert")
        self.engine.echo = True #to see what sql we are creating
        return self.engine
    
    def write_db_frame(self,a):
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print "Database Version: %s WRITING %s" %(data,a)
    
    def __del__(self):
        if self.connection is not None:
            self.connection.close()