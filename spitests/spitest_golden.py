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

# Configure the Eye Monitor Vertical and Phase Offsets
send_gspi(0x005a, 0x007f) # 007f is the default horizontal offset and is required
send_gspi(0x005b, 0x0400) # 00 is default and required, 04 reduces test time by 1/4
send_gspi(0x005c, 0xff04) # ff is default and required, 04 reduces test time by 1/4

# Rest for a second
time.sleep(1)

# Turn on eye monitor
send_gspi(0x005D, 0x0003)
# Wait 5 seconds
time.sleep(5)
# Read status (Data is in status[5])
status = read_gspi(0x0090)

# Get Data
for i in range(16): # Read 64 vertical lines
    counter = 0
    while((status[5] & 0x3 == 0) or (status[5] & 0x3 == 1)):
        time.sleep(1) # Wait 1 second before re-reading status
        status = read_gspi(0x0090)
        counter = counter + 1
        if counter == 10:
            send_gspi(0x005D, 0x0003)
            counter = 0
    if(status[5] & 0x3 == 3):
        print("Aborted!")
        break
    elif(status[5] & 0x3 == 2):
        eye_row = []
        counter = 0
        time.sleep(1)
        # Read Eye Scan Buffer 32 rows
        # eye_row = read_gspi_autoinc(REG_OFFSET, 34)
        # eye_data.append(eye_row)
        length_raw = read_gspi(REG_OFFSET + 1)
        length = int(((length_raw[4] << 8) + length_raw[5]-4)/2)
        for i in range (length):
            data = read_gspi(REG_OFFSET + 2 + i)
            value = data[5] + (data[4] << 8)
            eye_row.append(value)
            
        if (len(eye_row) == 128):
            eye_data.append(eye_row[0:31])
            eye_data.append(eye_row[32:63])
            eye_data.append(eye_row[64:95])
            eye_data.append(eye_row[96:127])

        time.sleep(1)
        
        # Reset Eye Scanner
        send_gspi(0x005D, 0x0002)
        
        time.sleep(1)

        while(status[5] & 0x3 != 0):
            status = read_gspi(0x0090)
            time.sleep(1)
            counter = counter + 1
            if counter == 10:
                send_gspi(0x005D, 0x0002)
        
        # Turn the Eye Monitor back on
        send_gspi(0x005D, 0x0003)

send_gspi(0x005D, 0x0000)

spi.close()

# All the information is in eye_data 
# Clean up data
for i in range(len(eye_data)):
    for j in range(len(eye_data[i])):
        if eye_data[i][j] > 2000:
            eye_data[i][j] = 2000

print(eye_data)

plt.imshow(eye_data)
plt.show()
