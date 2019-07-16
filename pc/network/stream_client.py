from threading import Thread
import msgpack
import time
import zmq

from network.ssh_tunnel import SSHTunnel


class StreamClient(SSHTunnel):

    context = zmq.Context()
    run     = True

    def __init__(self, ip, port):
        try: super().__init__(ip, port)
        except:
            self.reachable = False
            return
        else:
            self.reachable = True
        
        self.topics = {}

        self.socket = StreamClient.context.socket(zmq.SUB)
        self.socket.connect('tcp://%s:%s' % ('127.0.0.1', port))

        self.thread = Thread(target=self.client_loop, args=())
        self.thread.daemon = True
        self.thread.start()
        

    def sub_topic(self, topic_name, callback):
        print('Subscribing to topic %s' % topic_name)
        self.topics[topic_name] = callback
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')


    def is_reachable(self): 
        return self.reachable


    def client_loop(self):
        while StreamClient.run:
            if not self.reachable:
                time.sleep(0.1)
                continue

            try: topic_name, data = msgpack.unpackb(self.socket.recv())
            except ValueError:
                print('Unable to unpack data;  data = ', data)
                return

            topic_name = topic_name.decode('utf-8')

            try: self.topics[topic_name](data)
            except KeyError: print('Topic "' + str(topic_name) + ' not subscribed to')


    def kill(self):
        self.tunnel_server.stop()
        StreamClient.run = False