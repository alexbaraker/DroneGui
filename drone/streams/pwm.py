from hardware.addresses import *
from generic.memory import Memory


class PWMStreams():

    REG_IS_ACTIVE  = 0
    REG_DUTY_CYCLE = 4


    @staticmethod
    def get_pwm1_status():
        duty_cycle = Memory.read_from_mem(ADDR_PWM1, PWMStreams.REG_DUTY_CYCLE)
        return int(duty_cycle)


    @staticmethod
    def get_pwm2_status():
        duty_cycle = Memory.read_from_mem(ADDR_PWM2, PWMStreams.REG_DUTY_CYCLE)
        return int(duty_cycle)

    
    @staticmethod
    def get_pwm3_status():
        duty_cycle = Memory.read_from_mem(ADDR_PWM3, PWMStreams.REG_DUTY_CYCLE)
        return int(duty_cycle)


    @staticmethod
    def get_pwm4_status():
        duty_cycle = Memory.read_from_mem(ADDR_PWM4, PWMStreams.REG_DUTY_CYCLE)
        return int(duty_cycle)