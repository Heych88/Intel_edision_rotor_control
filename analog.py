
#!/usr/bin/env python

# Author: Brendan Le Foll <brendan.le.foll@intel.com>
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

import mraa

class analog():

    def __init__(self, pin, resolution=12):
        self.pin = pin
        if pin not in range (0, 6):
            raise Exception("Incorrect pin selection. Pins available (0, 1, 2, 3, 4, 5)")
        else:
            self.aio = self.set_pin(self.pin)

        self.setbit(resolution)

    def set_pin(self, pin):
        self.aio = mraa.Aio(pin)
        return self.aio

    def get_counts(self):
        count = self.aio.read()
        return count

    def get_float(self):
        """
        Read the input voltage and return it as a normalized float (0.0f-1.0f).
        :return: The current input voltage as a normalized float (0.0f-1.0f), error will be signaled by -1.0f
        """
        return self.aio.readFloat()

    def getbit(self):
        """
        Gets the bit value mraa is shifting the analog read to.
        :return: the bit resolution on the analog to digital converter
        """
        return self.aio.getBit()

    def setbit(self, bit):
        """
        Set the bit value which mraa will shift the raw reading from the ADC to. I.e. 10bits
        :param bit: the bits resolution for the conveter i.e 10
        """
        if bit < 1:
            bit = 1
        elif bit > 12:
            bit = 12
        self.aio.setBit(bit)
