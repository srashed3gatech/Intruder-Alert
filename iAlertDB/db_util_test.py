'''from database_utility import iAlertDB

#TESTING write_db_frame function
db_conn = iAlertDB();
for i in range(10):
    db_conn.write_db_frame(i)'''
    
import sqlalchemy

print sqlalchemy.__version__