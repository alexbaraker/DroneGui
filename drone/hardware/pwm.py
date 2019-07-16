from generic.memory import Memory


class PWM():

    PERIOD_REG     = 0
    DUTY_CYCLE_REG = 4

    def __init__(self, base_addr):
        self.base_addr      = base_addr


    def set_period(self, value):
        self.__validate_period(value)
        Memory.write_to_mem(self.base_addr, PWM.PERIOD_REG, value)


    def set_duty_cycle(self, value):
        self.__validate_duty_cycle(value)
        Memory.write_to_mem(self.base_addr, PWM.DUTY_CYCLE_REG, value)


    def __validate_period(self, value):
        # TODO
        pass


    def __validate_duty_cycle(self, value):
        # TODO
        pass