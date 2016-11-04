import socket

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host,port))

    s.listen(2)
    data_count = 0
    while True:
        print "Waiting for connection"
        c, addr = s.accept()
        print "Connection from: " + str(addr)


        d2_list = []

        while True:
            data = c.recv(16)

            if not data:
                break

            print "from connected user: " + str(data)


            d2_list.append(data)

            print 'process list: ' + str(d2_list)

            while d2_list:
                write_to_db = d2_list[0].split('#')
                for i in range(len(write_to_db)):
                    print write_to_db[i]
                d2_list.pop(0)
                print 'what is left in my list: ' + str(d2_list)
            data_count = data_count + 1
            print 'Finish the process of data# ' + str(data_count)




    #        c.send(data)
        c.close()

if __name__ == "__main__":
    Main()

