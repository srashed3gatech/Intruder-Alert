'''Thread Tutorial from TutorialPoint: 
        https://www.tutorialspoint.com/python/python_multithreading.htm'''
'''###################Using thred Module##################'''

'''import thread
import time

#function for thread
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s" %(threadName, time.ctime(time.time()))
        
# create 2thread

try:
    thread.start_new_thread(print_time, ("Thread-1", 2))
    thread.start_new_thread(print_time, ("Thread-2", 4))
except:
    print "Error in starting thread"
    
while 1:
    pass'''

'''Although it is very effective for low-level threading, 
but the thread module is very limited compared to the newer threading module'''


'''###################Using Threading Module##################'''

'''import threading
import time

exitFlag = 0

#Define a new subclass of the Thread class.
class myThread (threading.Thread): 
    
    #Override the __init__(self [,args]) method to add additional arguments.
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    #override the run(self [,args]) method to implement what the thread should do when started.
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name
    

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" %(threadName, time.ctime(time.time()))
        counter -= 1
    
#create new thread
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

#start new threadsafety
thread1.start()
thread2.start()


print "Exiting main thread" '''

'''###################Synchronized Threading##################'''

'''import threading
import time

threadLock = threading.Lock() #A new lock is created by calling the Lock() method, which returns the new lock
threads = []

class myThread (threading.Thread): 
    
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        print "Starting " + self.name
        #get lock to synchronize threads
        threadLock.acquire()
        
        print_time(self.name, self.counter, 5)
        
        #free lock to release next thread
        threadLock.release()
        
        print "Exiting " + self.name
    

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" %(threadName, time.ctime(time.time()))
        counter -= 1
    
#create new thread
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

#start new threadsafety
thread1.start()
thread2.start()

#add threads to the threadlist
threads.append(thread1)
threads.append(thread2)

#wait for all threads to complete
for t in threads:
    t.join()

print "Exiting main thread"'''

'''###################Multithreaded Queue##################'''

import threading
import time
import Queue

exitFlag = 0
threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)

threads = []
threadID = 1

class myThread (threading.Thread): 
    
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    
    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.q)
        print "Exiting " + self.name
    

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)

#create new threads
for tname in threadList:
    thread = myThread(threadID, tname, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

#filling up the queue
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

#wait for queue to empty
while not workQueue.empty():
    pass

#notify threads it's time to exit
exitFlag=1

#wait for all threads to complete
for t in threads:
    t.join()

print "Exiting main thread"
