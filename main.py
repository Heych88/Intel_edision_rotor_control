# -*- coding: utf-8 -*-
"""
Created on Sun Nov 06 16:08:42 2016

@author: haidyn.mcleod
"""
from __future__ import print_function

import time

import pwm
import analog
import gpio

# setup all IOs and global classes
motor = pwm.pwm(3, period=1000)
rotation_count = analog.analog(0)
motor_analog = analog.analog(1)

led = gpio.gpio(13)
led.set_high()

AREF = 5

def pwm_update(value):

    motor.write_pulse_duty(value)
    time.sleep(0.5)
    value = value + 0.01

    if value >= 0.75:
        value = 0.1

    return value

def main():
    try:
        value = 0.1
        while True:
            value = pwm_update(value)

            try:
                rot_count = rotation_count.get_counts()
                motor_voltage = motor_analog.get_float() * AREF
            except:
                print("Are you sure you have an ADC?")
            print("Position count: {},  Motor voltage: {:.3f}".format(rot_count, motor_voltage))

    except KeyboardInterrupt:
        motor.write_pulse_duty(0)
        motor.disable_pwm()
        led.set_low()
        print("Stopping everything")

    finally:
        motor.write_pulse_duty(0)
        motor.disable_pwm()
        led.set_low()
        print("Stopping everything")

if __name__ == '__main__':
    import sys
   
    if len(sys.argv) == 2:
        if sys.argv[1] == "install":
            print('Install')
    else:
        main()