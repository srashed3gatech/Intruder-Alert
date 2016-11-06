import MySQLdb

db = MySQLdb.connect("127.0.0.1","root","","ialert")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database Version: %s " % data
db.close()
