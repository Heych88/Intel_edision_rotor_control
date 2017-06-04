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
import controller

# setup all IOs and global classes
motor = pwm.pwm(3, period=1000)
rotation_count = analog.analog(0)
motor_analog = analog.analog(1)

led = gpio.gpio(13)
led.set_high()

AREF = 5

def pwm_update(pid, target, time_limit):
    # run the system
    start_time = time.time()
    current_time = 0
    run_error = 0

    while current_time < time_limit:
        measurement = rotation_count.get_counts()
        value = -1 * pid.update(measurement)
        if value >= 1:
            value = 1
        run_error = measurement - target
        motor.write_pulse_duty(value)

        current_time = time.time() - start_time

    motor.write_pulse_duty(0)
    print(run_error)

    return run_error

def twiddle(target, time_limit, tol=0.2):
    # Don't forget to call `make_robot` before you call `run`!
    p = [0, 0, 0]
    dp = [1, 1, 1]
    pid = controller.PID(p[0], p[1], p[2])
    pid.set_desired(target)

    best_error = rotation_count.get_counts()
    run_error = 0

    while sum(dp) > tol:
        for i in range(len(p)):
            p[i] += dp[i]

            # Reset the PID controller with the new parameters
            pid.clear_PID()  # re - initalise the controller
            pid.Kp = p[0]
            pid.ki = p[1]
            pid.kd = p[2]

            pwm_update(pid, target, time_limit)

            if (run_error < best_error):
                # the parameters are better
                best_err = run_error
                dp[i] *= 1.1
            else:
                # parameters are worse
                dp[i] -= 2 * dp[i]

                if (run_error < best_error):
                    best_err = run_error
                    dp[i] *= 1.1
                else:
                    p[i] += dp[i]
                    dp[i] *= 0.9

    return p, best_error

def main():
    try:
        value = 0.1
        #while True:

        #try:
        p, best_error = twiddle(535, 5)
        #motor_voltage = motor_analog.get_float() * AREF
        #except:
        #    print("Are you sure you have an ADC?")
        print("Gains: {},  error: {}".format(p, best_error))

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