from nanoservice import Requester

c = Requester('ipc:///tmp/service.sock')
res, err = c.call('echo', 'hello world’)
print('Result is {}'.format(res))