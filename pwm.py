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
        """
        :param pin: IO pin to output the pwm signal
        :param period: the time period in us between cycles
        :param enable: True => pwm is enabled on the pin
        :param min_limit: minimum value (duty cycle) output by the pwm
        :param max_limit: maximum value (duty cycle) output by the pwm
        """
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

        self.set_pin(self.pin)
        self.set_period(self.period)
        self.enable_pwm()

    def set_pin(self, pin):
        """
        Set the IO pin used for pwm output
        :param pin: pin number
        """
        if pin not in (3,5,6,9,10,11):
            raise Exception("Incorrect pin {} selected. Pins available (3, 5, 6, 9, 10, 11)".format(pin))
        else:
            self.pin = pin
            self.pwm = mraa.Pwm(pin)

    def set_period(self, period):
        """
        set the period in micro seconds (us) of the pwm cycle
        :param period: int value of the period time
        """
        self.period = period

        if period >= 1000000:
            period = period // 1000000
            print('period ', period)
            self.pwm.period(period=period)
        elif period >= 1000:
            self.pwm.period_ms(period // 1000)
        else:
            self.pwm.period_us(period)

    def set_pulsewidth(self, period):
        """
        Sets the pwm on time
        :param period: on time of the wave
        """
        if period < self.min_limit * self.period:
            self.pwm.pulsewidth_us(self.min_limit * self.period)
        elif period > self.max_limit * self.period:
            self.pwm.pulsewidth_us(self.max_limit * self.period)
        else:
            self.pwm.pulsewidth_us(period)

    def enable_pwm(self):
        """
        Turn on the pwm channel
        """
        self.enable = True
        self.pwm.enable(True)

    def disable_pwm(self):
        """
        Turn off the pwm channel
        """
        self.enable = False
        self.pwm.enable(False)

    def write_pulse_duty(self, value):
        """
        sets the duty cycle for the pwm channel
        :param value: 0 -> 1, duty cycle value
        """
        if value < self.min_limit:
            self.pwm.write(self.min_limit)
        elif value > self.max_limit:
            self.pwm.write(self.max_limit)
        else:
            self.pwm.write(value)

    def read_pulse(self):
        """
        Reads the current pwm duty cycle
        :return: current duty cycle
        """
        return self.pwm.read()
