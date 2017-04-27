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
    """
    class for the analog pins on the Intel Edison boards
    """
    def __init__(self, pin, resolution=12):
        """
        Setup analog channel for use at the desired resolution
        :param pin: GPIO AD pin used for measuring
        :param resolution: converter resolution to be used, defult 12-bit
        """
        self.pin = pin
        if pin not in range (0, 6):
            raise Exception("Incorrect pin selection. Pins available (0, 1, 2, 3, 4, 5)")
        else:
            self.aio = self.set_pin(self.pin)

        self.setbit(resolution)

    def set_pin(self, pin):
        """
        initalises the pin for use
        :param pin: GPIO AD pin used for measuring
        :return: initalised mraa class for later  reuse
        """
        self.aio = mraa.Aio(pin)
        return self.aio

    def get_counts(self):
        """
        reads the current converter counts
        :return: current converter pin reading
        """
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
