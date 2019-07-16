import time

from drone.network.stream_server import StreamServer
from drone.network.ctrl_server import CtrlServer

from pc.network.stream_client import StreamClient
from pc.network.ctrl_client import CtrlClient


def get_led():
    return True


def led_handler(data):
    print(data)



if __name__ == '__main__':

    #stream_server = StreamServer(5111, 'LED', 0.1, get_led)
    stream_client = StreamClient('129.21.146.247', 5111, 'LED')

    #ctrl_server = CtrlServer(5112, led_handler)
    ctrl_client = CtrlClient('129.21.146.247', 5112)

    try:
        while True:
            data = input('Set LED on (y/n): ')
            ctrl_client.send_data(data)
    except KeyboardInterrupt: 
        pass