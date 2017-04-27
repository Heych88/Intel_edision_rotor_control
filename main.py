# -*- coding: utf-8 -*-
"""
Created on Sun Nov 06 16:08:42 2016

@author: haidyn.mcleod
"""
from __future__ import print_function

#import KeyLogger_tk2
#import Servo
#import Steer_Wheels
#import Drive_Wheels
#import Encoder
import time
#import Ultrasonic
#import Sonar
import curses

import pwm

# setup all IOs and global classes
motor = pwm.pwm(3, period=700)


def test():
    '''Servo driver test on channel 1'''
    
    try:

        #motor = pwm.pwm(3, period=700)
        value = 0.1

        while True:
            motor.write_pulse_duty(value)
            time.sleep(0.5)
            value = value + 0.01

            print("\rPWM: {}".format(value * 100))
            if value >= 0.75:
                value = 0.1
        
        
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
        test()