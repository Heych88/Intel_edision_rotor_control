# -*- coding: utf-8 -*-
"""
Created on Sun Nov 06 16:08:42 2016

@author: haidyn.mcleod
"""
from __future__ import print_function

import time

import pwm
import analog

# setup all IOs and global classes
motor = pwm.pwm(3, period=700)
rotation_count = analog.analog(0)

def pwm_update(value):

    motor.write_pulse_duty(value)
    time.sleep(0.5)
    value = value + 0.01

    #print("PWM: {}".format(value * 100))
    if value >= 0.75:
        value = 0.1

    return value

def analog():
    try:
        return rotation_count.get_counts()
    except:
        print("Are you sure you have an ADC?")

def main():
    try:
        value = 0.1
        while True:
            value = pwm_update(value)
            print("This is rhe count: ", analog())

    except KeyboardInterrupt:
        motor.write_pulse_duty(0)
        print("Stopping everything")

    finally:
        motor.write_pulse_duty(0)
        print("Stopping everything")

if __name__ == '__main__':
    import sys
   
    if len(sys.argv) == 2:
        if sys.argv[1] == "install":
            print('Install')
    else:
        main()