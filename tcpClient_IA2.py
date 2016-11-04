

import socket

def Main():
    host = "127.0.0.1"
    port = 5000

    s = socket.socket()
    s.connect((host,port))

    result_1 = '3#33#USER3#CONF3'
    result_2 = '4#44#USER4#CONF4'
    s.send(result_1)
    s.send(result_2)
    print 'Send: ' + str(result_1)
    print 'Send: ' + str(result_2)


    message = raw_input("-> ")
    if message == 'q':
        s.close()


if __name__ == '__main__':
    Main()