import MySQLdb


class iAlertDB:
    connection = None
    
    def __init__(self):
        return;
        
    def connect_db(self):
        if self.connection is not None:
            return self.connection
        self.connection = MySQLdb.connect("127.0.0.1","root","","ialert")
        return self.connection
    
    def write_db_frame(self,a):
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print "Database Version: %s WRITING %s" %(data,a)
    
    def __del__(self):
        if self.connection is not None:
            self.connection.close()