from machine import I2C, Pin

from micropython import const

"""
This class is used to control the MCP45HX51 digital potentiometer

R0HW: This bit forces Resistor 0 into the “shutdown” configuration of the Hardware pin
R0A This bit connects/disconnects the Resistor 0 Terminal A to the Resistor 0 Network
R0W This bit connects/disconnects the Resistor 0 Wiper to the Resistor 0 Network
R0B This bit connects/disconnects the Resistor 0 Terminal B to the Resistor 0 Network
https://ww1.microchip.com/downloads/en/DeviceDoc/20005304A.pdf  
      0 >  253 Om
     22 >  670 Om
     23 >  687 Om
     34 >  898 Om
     35 >  917 Om
    143 > 2971 Om
    255 > 5000 Om
"""
# min 250 Om
# _GCALL_TCON = const(0x60)
# _GCALL_WIPER = const(0x40)
# _GCALL_WIPERUP = const(0x42)
# _GCALL_WIPERDWN  = const(0x44)
# _GCALL_COM_WRITE = const(0x02)
# _GCALL_COM_RWRITE = const(0x03)
# _GCALL_COM_WIPERINC = const(0x42)
# _GCALL_COM_WIPERDEC = const(0x44)
# High-Speed Master Mode Code (0000 1XXX)

_MEM_WIPER = const(0x00)
_MEM_TCON = const(0x40)
_COM_WRITE = const(0x00)
_COM_READ = const(0x0C)
_COM_WIPERINC = const(0x04)
_COM_WIPERDEC = const(0x08)
_TCON_1111 = const(0xf0)  # 0b11110000 constant that is always written to the TCON register
# _TCON_R0HW = const(0x08)  # Shutdown Resistor Force
# _TCON_R0A =  const(0x04)  # Terminal A Connection
# _TCON_R0B =  const(0x01)  # Wiper Connection
# _TCON_R0W =  const(0x02)  # Terminal B Connection

_p_r0hw = const(3)
_p_r0a = const(2)
_p_r0w = const(1)
_p_r0b = const(0)


# This class is used to control the MCP45HX51 digital potentiometer
class Mcp45hx51:
    def __init__(self, i2c, address, debug=False):
        """
        The function configures the TCON registers and value potentiometer

        :param i2c: the I2C bus object
        :param address: the I2C address of the TCON
        """
        self.wiper_value = None
        self.i2c = i2c
        self.address = address
        self.debug = debug
        # self.r0hw = True  # 0b00001000
        # self.r0a = True   # 0b00000100
        # self.r0w = True   # 0b00000010
        # self.r0b = True   # 0b00000001
        # self.tcon_read()
        self._configure_tcon()

    def _configure_tcon(self, wiper=255, r0hw=True, r0a=False, r0w=True, r0b=True):
        """
        The function sets the wiper position, and then sets the R0HW, R0A, R0W, and R0B bits in the TCON register

        :param wiper: The wiper value is the resistance between the wiper and the B terminal, defaults to 255 (optional)
        :param r0hw: Hardware reset, defaults to True (optional)
        :param r0a: , defaults to False (optional)
        :param r0w: , defaults to True (optional)
        :param r0b: , defaults to True (optional)
        """
        self.wiper_set(wiper)
        self.r0hw = r0hw
        self.r0a = r0a
        self.r0w = r0w
        self.r0b = r0b
        self._tcon_write()

    def wiper_set(self, value):
        """
        `self.i2c.writeto_mem(self.address, _COM_WRITE, bytes([value]))`

        The `self.i2c.writeto_mem` function is a MicroPython function that writes data to the MCP4725 DAC. The
        `self.address` is the I2C address of the MCP4725 DAC. The `_COM_WRITE` is the command to write to the DAC. The
        `bytes([value])` is the value to write to the DAC

        :param value: The value to set the wiper to
        """
        self.i2c.writeto_mem(self.address, _COM_WRITE, bytes([value]))
        self.wiper_value = value
        # self.wiper_value = self.wiper_read()
        self._print_debug(f'mcp_{self.address}: wiper_set {value}')

    def wiper_read(self):
        """
        It reads the value of the wiper register from the MCP4251 chip
        :return: The value of the wiper register.
        """
        return self.i2c.readfrom_mem(self.address, _MEM_WIPER | _COM_READ, 2)[1]

    def wiper_increment(self, offset):
        """
        It increments the wiper register by the offset value.

        :param offset: The number of steps to increment the wiper
        """
        for _ in range(offset):
            self.i2c.writeto(self.address, bytes([_COM_WIPERINC]))

    def wiper_decrement(self, offset):
        """
        It decrements the wiper register by the offset value.

        :param offset: The number of steps to decrement the wiper
        """
        for _ in range(offset):
            self.i2c.writeto(self.address, bytes([_COM_WIPERDEC]))

    def tcon_read(self):
        """
        The function reads the TCON register and sets the r0b, r0w, r0a, and r0hw variables to the appropriate values
        """
        _tcon = self.i2c.readfrom_mem(self.address, _MEM_TCON | _COM_READ, 2)[1]
        self.r0b = bool(_tcon & 0b00000001)
        self.r0w = bool(_tcon & 0b00000010)
        self.r0a = bool(_tcon & 0b00000100)
        self.r0hw = bool(_tcon & 0b00001000)
        _answer = f'mcp_{self.address}: tcon: r0hw={self.r0hw} r0a={self.r0a} r0w={self.r0w} r0b={self.r0b}'
        self._print_debug(_answer)
        return _answer

    def poweroff(self, value):
        """
        The function turns on and turn off potentiometer

        :param value: 0 = off, 1 = on
        """
        self.r0hw = value
        self._tcon_write()
        self._print_debug(f'mcp_{self.address}: poweroff {value}')

    def connect_terminal_a(self, value):
        """
        This function connects A

        :param value: False = disconnect, True = connect
        """
        self.r0a = value
        self._tcon_write()
        self._print_debug(f'mcp_{self.address}: connect_terminal_a {value}')

    def connect_terminal_b(self, value):
        """
        This function connects B

        :param value: False = disconnect, True = connect
        """
        self.r0b = value
        self._tcon_write()
        self._print_debug(f'mcp_{self.address}: connect_terminal_b {value}')

    def connect_wiper(self, value):
        """
        This function connects the wiper of the potentiometer to the output

        :param value: False = disconnect, True = connect
        """
        self.r0w = value
        self._tcon_write()
        self._print_debug(f'mcp_{self.address}: connect_wiper {value}')

    def _tcon_write(self):
        """
        The function writes the values of the four variables to the TCON register
        """
        # print(f'addr{self.address} write: r0hw={self.r0hw} r0a={self.r0a} r0w={self.r0w} r0b={self.r0b}')
        self.__tcon_data = _TCON_1111 ^ self.r0b << _p_r0b ^ self.r0w << _p_r0w ^ self.r0a << _p_r0a ^ self.r0hw << _p_r0hw
        self.i2c.writeto_mem(self.address, _MEM_TCON | _COM_WRITE, bytes([self.__tcon_data]))

    def _print_debug(self, text):
        """
        If the debug variable is set to True, print the text

        :param text: The text to be printed
        """
        if self.debug:
            print(text)


if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(19), sda=Pin(5), freq=400000)
    print(i2c.scan())
    device1 = Mcp45hx51(i2c, 60)
    device2 = Mcp45hx51(i2c, 61)

    device1.poweroff(True)
    device1.connect_wiper(True)
    device1.connect_terminal_b(False)
    device1.tcon_read()

    device1.wiper_set(0)
    device1.wiper_increment(20)
    device1.wiper_decrement(20)
    print(device1.address, device1.wiper_read())
