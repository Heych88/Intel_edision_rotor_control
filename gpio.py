
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function
import mraa

class gpio():

    def __init__(self, pin, dir=mraa.DIR_OUT, resistor=None):

        self.pin_num = pin

        self.set_pin(pin)
        self.resistor = resistor
        self.set_dir(dir, resistor=resistor)

        # Interrupt types
        self.RISING = mraa.EDGE_RISING
        self.FALLING = mraa.EDGE_FALLING
        self.BOTH = mraa.EDGE_BOTH

        # IO resistor type
        self.OUT = mraa.DIR_OUT
        self.IN = mraa.DIR_IN
        self.PULL_UP = mraa.DIR_OUT_HIGH
        self.PULL_DOWN = mraa.DIR_OUT_LOW

    def set_pin(self, pin):
        """
        Set the IO pin used for Gpio
        :param pin: pin number
        """
        if pin not in range(0, 14):
            raise Exception("Incorrect pin {} selected. Pins available (0 to 13)".format(pin))
        else:
            self.pin = pin
            self.gpio_pin = mraa.Gpio(pin)

    def set_dir(self, dir, resistor=None):
        """
        Set the IO pins direction of use as either input or output.
        If resistor is not None, only an output direction on the pin can be used.
        :param dir: input (IN) or output (OUT) direction
        :param resistor: None -> do not use a pull up resistor,
                        'UP' -> use a pull up resistor,
                        'DOWN' -> use a pull down resistor
        """
        self.IN = mraa.DIR_IN
        self.OUT = mraa.DIR_OUT
        self.PULL_UP = mraa.DIR_OUT_HIGH
        self.PULL_DOWN = mraa.DIR_OUT_LOW
        if dir not in (mraa.DIR_OUT, mraa.DIR_IN):
            # incorrect arguments passed in
            raise Exception("Incorrect pin direction dir={}. Use 'gpio.IN' or 'gpio.OUT'".format(dir))
        elif resistor not in (None, self.PULL_UP, self.PULL_DOWN):
            # incorrect arguments passed in
            raise Exception("Incorrect resistor={}. Use 'UP' or 'Down'".format(resistor))
        elif dir is self.IN:
            self.dir = dir
            self.gpio_pin.dir(self.IN)
            if resistor is not None:
                raise Warning('default', 'Pin dir is {} but should be \'None\' when using resistor'.format(dir))
        elif resistor is not None:
            self.resistor = resistor
            self.dir = dir
            # default to only output
            if resistor is self.PULL_UP:
                self.gpio_pin.dir(mraa.DIR_OUT_HIGH)
            else:
                self.gpio_pin.dir(mraa.DIR_OUT_LOW)
        else:
            self.resistor = resistor
            self.dir = dir
            # default to only output
            self.gpio_pin.dir(mraa.DIR_OUT)

    def set_high(self):
        self.gpio_pin.write(1)

    def set_low(self):
        self.gpio_pin.write(0)

    def read(self):
        self.gpio_pin.read()

    def read_dir(self):
        self.gpio_pin.readDir()

    def isr_catch(self, *args):
        print('Hello')

    def interrupt(self, edge, *args):
        if edge not in (self.BOTH, self.FALLING, self.RISING):
            # incorrect arguments passed in
            raise Exception("Incorrect edge supplied. edge={}. Use gpio.BOTH, gpio.FALLING or gpio.RISING".format(edge))
        else:
            self.gpio_pin.isr(edge, self.isr_catch(), args)


        #self.gpio_pin.edge()
        #self.gpio_pin.isr()
        #self.gpio_pin.isrExit()
        #self.gpio_pin.getPin()
        #self.gpio_pin.mode()
