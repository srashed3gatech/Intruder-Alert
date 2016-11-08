import socket
from VideoFrame import VideoFrame

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host,port))
    d2_list = []
    call_back(10s, write_db_from_buffer(d2_list[], read_pointer, write_pointer))
    write_pointer=100
    read_pointer=0
    s.listen(3)
    data_count = 0
    while True:
        print "Waiting for connection"
        c, addr = s.accept()
        print "Connection from: " + str(addr)

        while True:
            recv_len = 1024
            data = c.recv(recv_len)

            if not data:
                break

            print "from connected user: " + str(data)
            if len(data) == recv_len:
                print 'buffer overflow!!'

            datagram = d2_list[0].split('#')
            frame = VideoFrame()
            frame.video_id = datagram[1]
            frame.frame_num = datagram[2]
            frame.timestamp = datagram[3]
            frame.user_id = datagram[4]
            frame.confid_level = datagram[5]
    
            d2_list[write_pointer % 100] = frame
            write_pointer =  write_pointer-1 if write_pointer > 0 else 100

           ''' print 'process list: ' + str(d2_list)

            while d2_list:
                write_to_db = d2_list[0].split('#')
                for i in range(len(write_to_db)):
                    if write_to_db[i] == '':     # pass the first # in the protocol
                        pass
                    else:
                        if i%6 == 1:
                            print 'write to DB vid'
                            print write_to_db[i]
                        if i%6 == 2:
                            print 'write to DB frame_id'
                            print write_to_db[i]
                        if i%6 == 3:
                            print 'write to DB time_stamp'
                            print write_to_db[i]
                        if i%6 == 4:
                            print 'write to DB user_id'
                            print write_to_db[i]
                        if i%6 == 5:
                            print 'write to DB conf_level'
                            print write_to_db[i]
                d2_list.pop(0)
                print 'what is left in my list: ' + str(d2_list) '''
            data_count = data_count + 1
            print 'Finish the process of data# ' + str(data_count)




    #        c.send(data)
        c.close()

if __name__ == "__main__":
    Main()

