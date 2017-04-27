#!/usr/bin/env python

# Author: Thomas Ingleby <thomas.c.ingleby@intel.com>
# Copyright (c) 2014 Intel Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import print_function
import mraa

class pwm():

    def __init__(self, pin, period=1000, enable=True, min_limit=0., max_limit=1.):
        self.pin = pin
        self.period = period
        self.enable = enable
        if min_limit < 0:
            self.min_limit = 0.
        else:
            self.min_limit = min_limit
        if max_limit > 1:
            self.max_limit = 1.
        else:
            self.max_limit = max_limit

        if pin not in (3,5,6,11):
            raise Exception("Incorrect pin selection. Pins available (3, 5, 6, 11)")
        else:
            self.set_pin(self.pin)

        self.set_period(self.period)
        self.enable_pwm()

    def set_pin(self, pin):
        self.pwm = mraa.Pwm(pin)

    def set_period(self, period):
        self.pwm.period_us(period)

    def set_pulsewidth(self, period):

        if period < 0:
            period = 0
        elif period > self.max_limit * self.period:
            period = self.max_limit * self.period
        else:
            self.pwm.pulsewidth_us(period)

    def enable_pwm(self):
        self.pwm.enable(True)

    def disable_pwm(self):
        self.pwm.enable(False)

    def write_pulse_duty(self, value):

        if value < self.min_limit:
            value = self.min_limit
        elif value > self.max_limit:
            self.pwm.write(1)
        else:
            self.pwm.write(value)

    def read_pulse(self):
        return self.pwm.read()
