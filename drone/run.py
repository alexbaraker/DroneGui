import time

from network.address import *
from network.stream_server import StreamServer
from network.ctrl_server import CtrlServer

from streams.pwm import PWMStreams
from streams.cam import CamStream

from hardware.addresses import *
from generic.memory import Memory


class DroneServer():
    
    @staticmethod
    def init():
        DroneServer.uplink_server = CtrlServer(UPLINK_PORT, DroneServer.uplink_handler)
        DroneServer.ctrl_server   = CtrlServer(CTRL_PORT, DroneServer.ctrl_handler)

        DroneServer.pwm_status_server = StreamServer(PWM_STREAM_PORT, 0.1)
        DroneServer.pwm_status_server.add_topic('PWM1', PWMStreams.get_pwm1_status)
        DroneServer.pwm_status_server.add_topic('PWM2', PWMStreams.get_pwm2_status)
        DroneServer.pwm_status_server.add_topic('PWM3', PWMStreams.get_pwm3_status)
        DroneServer.pwm_status_server.add_topic('PWM4', PWMStreams.get_pwm4_status)

        DroneServer.cam_stream = CamStream()
        DroneServer.cam_server = StreamServer(CAM_STREAM_PORT, 0.1)
        DroneServer.cam_server.add_topic('CAM', DroneServer.cam_stream.get_frame)

        DroneServer.watchdog = time.time()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt: exit(0)


    @staticmethod
    def uplink_handler(data):
        #if (time.time() - DroneServer.watchdog)*1000 > 100:
        #    print('Client took more than 100ms to ping')
        print('Ping: ' + str((time.time() - DroneServer.watchdog)*1000) + 'ms')
        DroneServer.watchdog = time.time()

        if data == 'ping': return 'pong'
        else:              return '????'


    @staticmethod
    def ctrl_handler(data):
        _id, val = data

        if _id == 'KILLSWITCH':
            print('KILLSWITCH TRIGGERED')
            Memory.write_to_mem(ADDR_KILLSWITCH, 0, 0x0)

        if _id == 'ROT':
            ball_x, ball_y = val
            Memory.write_to_mem(ADDR_CAM, 0, ball_x)
            Memory.write_to_mem(ADDR_CAM, 4, ball_y)



if __name__ == '__main__':
    DroneServer.init()