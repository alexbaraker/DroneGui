import time
from generic.memory import Memory


class Accelerometer():

    X_REG    = 0
    Y_REG    = 0
    Z_REG    = 0
    CTRL_REG = 0

    READ_BIT = 0

    def __init__(self, base_addr):
        self.base_addr = base_addr


    def read(self):
        Memory.set_bit(self.base_addr, Accelerometer.CTRL_REG, Accelerometer.READ_BIT, True)
        while not Memory.read_bit(self.base_addr, Accelerometer.CTRL_REG, Accelerometer.READ_BIT):
            time.sleep(0.000001) # Wait for a microsecond

        read_regs = [ Accelerometer.X_REG, Accelerometer.Y_REG, Accelerometer.Z_REG ]
        accel_vals = Memory.read_bulk(self.base_addr, read_regs)
        Memory.set_bit(self.base_addr, Accelerometer.CTRL_REG, Accelerometer.READ_BIT, False)

        return accel_vals