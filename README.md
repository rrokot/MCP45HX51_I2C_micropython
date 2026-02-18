# MCP45HX51 I2C MicroPython Library

MicroPython library for controlling the MCP45HX51 digital potentiometer via I2C interface.

## Overview

This library provides a simple and intuitive interface to control the MCP45HX51 family of digital potentiometers from Microchip. The MCP45HX51 is a single-channel, 8-bit (256 wiper steps) digital potentiometer with I2C interface.

**Datasheet:** [MCP45HX51 Official Documentation](https://ww1.microchip.com/downloads/en/DeviceDoc/20005304A.pdf)

## Features

- **Wiper Control**: Set, increment, and decrement wiper position (0-255)
- **Terminal Configuration**: Connect/disconnect terminals A, B, and Wiper
- **Power Management**: Shutdown/power-on control
- **TCON Register**: Full control over Terminal Control (TCON) register
- **Debug Mode**: Optional debug output for troubleshooting
- **Multiple Devices**: Support for multiple devices on the same I2C bus

## Resistance Range

The MCP45HX51 provides a resistance range from approximately 250Ω to 5000Ω:

| Wiper Value | Resistance |
|-------------|------------|
| 0           | ~253 Ω     |
| 22          | ~670 Ω     |
| 23          | ~687 Ω     |
| 34          | ~898 Ω     |
| 35          | ~917 Ω     |
| 143         | ~2971 Ω    |
| 255         | ~5000 Ω    |

## Installation

1. Copy the `MCP45HX51I2C.py` file to your MicroPython device
2. Import the library in your code:

```python
from MCP45HX51I2C import Mcp45hx51
from machine import I2C, Pin
```

## Hardware Connection

Connect your MCP45HX51 to your MicroPython board via I2C:

- **SCL**: Connect to your board's I2C clock pin
- **SDA**: Connect to your board's I2C data pin
- **VDD**: Connect to 3.3V or 5V (depending on your device)
- **VSS**: Connect to GND
- **A0, A1**: I2C address configuration pins

### I2C Address

The I2C address is configurable via the A0 and A1 pins (default base address: 0x3C).

## Usage

### Basic Example

```python
from machine import I2C, Pin
from MCP45HX51I2C import Mcp45hx51

# Initialize I2C bus
i2c = I2C(0, scl=Pin(19), sda=Pin(5), freq=400000)

# Scan for I2C devices
print("I2C devices found:", i2c.scan())

# Initialize MCP45HX51 device (address 60 = 0x3C)
potentiometer = Mcp45hx51(i2c, 60)

# Set wiper position
potentiometer.wiper_set(128)  # Set to mid-point

# Read current wiper position
current_value = potentiometer.wiper_read()
print(f"Current wiper value: {current_value}")
```

### Advanced Example

```python
from machine import I2C, Pin
from MCP45HX51I2C import Mcp45hx51

# Initialize I2C
i2c = I2C(0, scl=Pin(19), sda=Pin(5), freq=400000)

# Create two devices with different addresses
device1 = Mcp45hx51(i2c, 60, debug=True)
device2 = Mcp45hx51(i2c, 61, debug=True)

# Configure device1
device1.poweroff(True)              # Power on the device
device1.connect_wiper(True)         # Connect wiper to resistor network
device1.connect_terminal_b(False)   # Disconnect terminal B
device1.tcon_read()                 # Read TCON register

# Set wiper value
device1.wiper_set(0)                # Set to minimum
device1.wiper_increment(20)         # Increment by 20 steps
device1.wiper_decrement(20)         # Decrement by 20 steps

# Read final value
print(device1.address, device1.wiper_read())
```

## API Reference

### Constructor

```python
Mcp45hx51(i2c, address, debug=False)
```

**Parameters:**
- `i2c`: I2C bus object
- `address`: I2C address of the device (integer)
- `debug`: Enable debug output (boolean, default: False)

### Methods

#### Wiper Control

##### `wiper_set(value)`
Set the wiper to a specific position.
- **Parameters:** `value` (int, 0-255)
- **Returns:** None

##### `wiper_read()`
Read the current wiper position.
- **Returns:** Current wiper value (int, 0-255)

##### `wiper_increment(offset)`
Increment the wiper position by specified steps.
- **Parameters:** `offset` (int) - Number of steps to increment
- **Returns:** None

##### `wiper_decrement(offset)`
Decrement the wiper position by specified steps.
- **Parameters:** `offset` (int) - Number of steps to decrement
- **Returns:** None

#### Terminal Configuration

##### `connect_terminal_a(value)`
Connect or disconnect terminal A.
- **Parameters:** `value` (bool) - True to connect, False to disconnect
- **Returns:** None

##### `connect_terminal_b(value)`
Connect or disconnect terminal B.
- **Parameters:** `value` (bool) - True to connect, False to disconnect
- **Returns:** None

##### `connect_wiper(value)`
Connect or disconnect the wiper.
- **Parameters:** `value` (bool) - True to connect, False to disconnect
- **Returns:** None

#### Power Management

##### `poweroff(value)`
Control device power state via hardware shutdown bit.
- **Parameters:** `value` (bool) - True to enable (power on), False to shutdown (power off)
- **Returns:** None
- **Note:** Despite the method name, `True` powers the device ON, `False` powers it OFF

#### TCON Register

##### `tcon_read()`
Read the Terminal Control (TCON) register status.
- **Returns:** String with TCON register status

## TCON Register Bits

The Terminal Control (TCON) register controls the connection of terminals:

- **R0HW**: Hardware shutdown bit - Forces resistor into shutdown configuration
- **R0A**: Terminal A Connection - Connects/disconnects Terminal A to resistor network
- **R0W**: Wiper Connection - Connects/disconnects Wiper to resistor network
- **R0B**: Terminal B Connection - Connects/disconnects Terminal B to resistor network

## Typical Applications

- Audio volume control
- Sensor calibration
- Programmable voltage dividers
- Gain adjustment
- Offset adjustment
- Power supply trimming

## Compatibility

This library is designed for MicroPython and has been tested with:
- ESP32 boards
- ESP8266 boards
- Other MicroPython-compatible boards with I2C support

## License

This project is open source. Please check the repository for license information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [MCP45HX51 Datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/20005304A.pdf)
- [MicroPython I2C Documentation](https://docs.micropython.org/en/latest/library/machine.I2C.html)

## Author

Created by rrokot

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/rrokot/MCP45HX51_I2C_micropython).
