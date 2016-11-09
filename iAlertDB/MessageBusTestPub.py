from nanoservice import Responder

def echo(msg):
    return msg

s = Responder('ipc:///tmp/service.sock')
s.register('echo', echo)
s.start()