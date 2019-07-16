from threading import Thread
import time
import msgpack
import zmq


class CtrlServer():

    context = zmq.Context()

    def __init__(self, port, handler):
        self.handler = handler

        self.socket = CtrlServer.context.socket(zmq.REP)
        self.socket.bind('tcp://*:%s' % port)

        print('Created server at tcp://*:%s' % port)
        
        self.thread = Thread(target=self.server_loop, args=())
        self.thread.daemon = True
        self.thread.start()


    def server_loop(self):
        while True:
            data = msgpack.unpackb(self.socket.recv(), raw=False)
            data = msgpack.packb(self.handler(data), use_bin_type=True)
            self.socket.send(data)