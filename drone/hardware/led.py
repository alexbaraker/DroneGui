from generic.memory import Memory


class LED():

    def __init__(self, base_addr, register, bit):
        self.base_addr = base_addr
        self.register  = register
        self.bit       = bit


    def set_on(self):
        Memory.set_bit(self.base_addr, self.register, self.bit, True)


    def set_off(self):
        Memory.set_bit(self.base_addr, self.register, self.bit, False)