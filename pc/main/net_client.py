import time
import numpy as np
import json
import base64
from threading import Thread

from misc.callback import callback
from network.address import *
from network.stream_client import StreamClient
from network.ctrl_client import CtrlClient


class NetClient():

    def __init__(self):
        self.uplink_client = CtrlClient(IP_ADDR, UPLINK_PORT)
        self.uplink_client.connection_changed.connect(self.connection_changed_handler)

        if not self.uplink_client.is_reachable():
            return

        print('Checking server status . . .')
        self.ping_server()

        self.pwm_client = StreamClient(IP_ADDR, PWM_STREAM_PORT)
        self.pwm_client.sub_topic('PWM1', self.pwm1_callback)
        self.pwm_client.sub_topic('PWM2', self.pwm2_callback)
        self.pwm_client.sub_topic('PWM3', self.pwm3_callback)
        self.pwm_client.sub_topic('PWM4', self.pwm4_callback)

        self.cam_client = StreamClient(IP_ADDR, CAM_STREAM_PORT)
        self.cam_client.sub_topic('CAM', self.cam_callback)

        self.ctrl_client = CtrlClient(IP_ADDR, CTRL_PORT)

        self.run = True

        self.thread = Thread(target=self.net_client_loop, args=())
        self.thread.daemon = True
        self.thread.start()


    def ping_server(self):
        reply = self.uplink_client.send_data('ping')
        if not self.uplink_client.connected: return False

        return (reply == b'pong')


    def connection_changed_handler(self, client):
        ip, port = client.ip, client.port
        connected = client.is_connected()

        if connected: print('Connected to %s:%s' % (ip, port))
        else:         print('Disconnected from %s:%s' % (ip, port))

    
    def net_client_loop(self):
        try:
            while self.run:
                self.ping_server()
                time.sleep(0.1)
        finally:
            self.uplink_client.kill()
            self.ctrl_client.kill()
            self.pwm_client.kill()
            self.cam_client.kill()


    def kill(self):
        self.run = False


    @callback
    def pwm1_callback(self, data):
        NetClient.pwm1_callback.emit(str(data))


    @callback
    def pwm2_callback(self, data):
        NetClient.pwm2_callback.emit(str(data))


    @callback
    def pwm3_callback(self, data):
        NetClient.pwm3_callback.emit(str(data))


    @callback
    def pwm4_callback(self, data):
        NetClient.pwm4_callback.emit(str(data))


    @callback
    def cam_callback(self, data):
        #json_load = json.loads(data)
        #data = np.asarray(json_load['data'])
        
        image = base64.b64decode(data)
        #cv_image = np.frombuffer(image, dtype=np.uint8)
        image = np.fromstring(image, dtype=np.uint8)
        NetClient.cam_callback.emit(image)

    
    def send_killsig_to_drone(self):
        if self.uplink_client.connected:
            return self.ctrl_client.send_data(('KILLSWITCH', True))
        else:
            print('CAN\'T KILLSWITCH - NOT CONNECTED TO SERVER!')

    
    def send_detection_to_drone(self, ball_x, ball_y):
        if self.uplink_client.connected:
            return self.ctrl_client.send_data(('ROT', (ball_x, ball_y)))