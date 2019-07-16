from threading import Thread
import msgpack
import random
import time
import zmq


class StreamServer():
    '''
    Designed to start streaming data on some TCP port. Lacks support
    for multiple topics per port
    '''
    context = zmq.Context()

    def __init__(self, port, rate):
        self.rate = rate

        self.socket = StreamServer.context.socket(zmq.PUB)
        self.socket.bind('tcp://*:%s' % port)

        print('Created server at tcp://*:%s' % port)
        
        self.topics = []

        self.thread = Thread(target=self.server_loop, args=())
        self.thread.daemon = True
        self.thread.start()


    def add_topic(self, topic_name, callback):
        self.topics.append((topic_name, callback))


    def server_loop(self):
        while True:
            for topic in self.topics[:]:
                topic_name, callback = topic

                data = msgpack.packb((topic_name, callback()), use_bin_type=True)
                self.socket.send(data)
                time.sleep(self.rate)