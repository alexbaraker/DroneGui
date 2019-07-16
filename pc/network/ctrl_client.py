import msgpack
import time
import zmq

from misc.callback import callback
from network.ssh_tunnel import SSHTunnel
        

class CtrlClient(SSHTunnel):

    context = zmq.Context()

    def __init__(self, ip, port):
        self.reachable = False

        for _ in range(3):
            try: super().__init__(ip, port)
            except:
                time.sleep(1)
            else:
                self.reachable = True
                break
        
        if not self.reachable:
            return

        self.ip   = ip
        self.port = port
        
        self.socket = CtrlClient.context.socket(zmq.REQ)
        self.socket.linger = 250 
        self.socket.connect('tcp://%s:%s' % (ip, port))

        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

        self.error_flag    = False
        self.connected     = True
        

    def is_reachable(self): return self.reachable
    def is_connected(self): return self.connected
    

    def reconnect(self):
        self.poller.unregister(self.socket)
        self.socket.close()
        self.socket = CtrlClient.context.socket(zmq.REQ)
        self.socket.connect('tcp://%s:%s' % (self.ip, self.port))
        self.poller.register(self.socket, zmq.POLLIN)


    def send_data(self, data, timeout=10, tries=10):
        # Don't try to send data if we have not recieved a reply
        #if self.connected:
        try: self.socket.send(msgpack.packb(data, use_bin_type=True))
        except zmq.error.ZMQError:
            if not self.error_flag:
                self.error_flag = True
                print('Unable to send data')
            else:
                print('Attempting to reconnect . . .')
                try: self.reconnect()
                except Exception as e: print('Error:', e)
            return None
        else:
            self.error_flag = False

        for _ in range(tries):
            socks = dict(self.poller.poll(timeout))
            if not socks: continue

            if socks.get(self.socket) == zmq.POLLIN:
                data = msgpack.unpackb(self.socket.recv(zmq.NOBLOCK), raw=False)
                self.connection_changed(True)
                return data

        self.connection_changed(False)
        return None


    @callback
    def connection_changed(self, connected):
        if self.connected == connected: return
        
        self.connected = connected
        CtrlClient.connection_changed.emit(self)


    def kill(self):
        self.tunnel_server.stop()
        self.socket.close()