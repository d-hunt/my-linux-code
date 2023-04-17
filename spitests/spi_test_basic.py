import time
import spidev
import numpy as np
import matplotlib.pyplot as plt

UNIT_ADDRESS = 0x1
READ_CW = 0xA000 + (UNIT_ADDRESS << 7)
READ_AUTO_INC = 0xB000 + (UNIT_ADDRESS << 7)
WRITE_CW = 0x2000 + (UNIT_ADDRESS << 7)
REG_OFFSET = 0x6CC1

eye_row = []
eye_data = []
data_buffer = []
vert_val = [0,0,0,0,0,0]

# We only have SPI bus 0 availale to us on the RPI
bus = 0

# Device is the chip select pin.  Set to 0 or 1 depending on connections
device = 0

# Enable SPI
spi = spidev.SpiDev()

# Open a connection to a specific bus and device
spi.open(bus, device)

# Set SPI speed and mode
spi.max_speed_hz = 500000
spi.mode = 0

def send_gspi(addr, data):
    msg = []
    msg.append(WRITE_CW >> 8)
    msg.append(WRITE_CW & 0xff)
    msg.append(addr >> 8)
    msg.append(addr & 0xff)
    msg.append(data >> 8)
    msg.append(data & 0xff)
    spi.xfer3(msg)

def read_gspi(addr):
    msg = []
    msg.append(READ_CW >> 8)
    msg.append(READ_CW & 0xff)
    msg.append(addr >> 8)
    msg.append(addr & 0xff)
    msg.append(0x00)
    msg.append(0x00)
    results = spi.xfer3(msg)
    return results

def read_gspi_autoinc(addr, length):
    msg = []
    msg.append(READ_CW >> 8)
    msg.append(READ_CW & 0xff)
    msg.append(addr >> 8)
    msg.append(addr & 0xff)
    for i in range(length):
        msg.append(0x00)
        msg.append(0x00)
    results = spi.xfer3(msg)
    return results

# initial set-up commands

# Write to EYE_MON_INT_CFG_3 per sec 4.9.12.1
send_gspi(0x0057, 0x8006)
status = read_gspi(0x0001)
