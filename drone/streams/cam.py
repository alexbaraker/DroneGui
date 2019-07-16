import ctypes
import json
import numpy as np
import cv2


# Thx https://stackoverflow.com/a/47626762
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class CamStream():

    def __init__(self):
        self.lib = ctypes.cdll.LoadLibrary('/snickerdoodle/mt9v034/mt9v034-driver.so')
        self.frame = np.ones((480, 752, 4), dtype=np.uint8)

        result = self.lib.init()
        if result != 0:
            print('CamStream init error:', result)


    def get_frame(self):
        result = self.lib.getFrame(ctypes.c_void_p(self.frame.ctypes.data))
        if result != 0:
            print('CamStream getFrame error:', result)

        tempImage = np.ascontiguousarray(self.frame[:,:,0:3], dtype=np.uint8)
        result, jpg = cv2.imencode('.jpg', tempImage)        
        base64_jpg = base64.b64encode(jpg)
        
        return base64_jpg