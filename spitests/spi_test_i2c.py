import time
import smbus
import numpy as np
import matplotlib.pyplot as plt

import smbus
import time

WRITE_CW = 0x2000
READ_CW = 0xA000
AUTO_INC_CW = 0xB000
REG_OFFSET = 0x6CC1

channel = 1
address = 0x20
bus = smbus.SMBus(channel)


eye_row = []
eye_data = []
data_buffer = []
vert_val = [0,0,0,0,0,0]

def bin_array(value):
    # Convert the integer to a binary string with leading zeros
    binary_string = format(value, '016b')

    # Convert the binary string to an array of ones and zeros
    ones_and_zeros = [int(bit) for bit in binary_string]
    return(ones_and_zeros)

def unarray_bin(bin_list):
    # Convert the array to a binary string
    binary_string = ''.join(str(bit) for bit in bin_list)
    # Convert the binary string to a hexadecimal value
    value = int(binary_string, 2)

    return(value) 

def send_gspi(addr, data, cs):
    arr1 = bin_array(WRITE_CW)
    arr2 = bin_array(addr)
    arr3 = bin_array(data)
    bits = []
    bits.extend(arr1)
    bits.extend(arr2)
    bits.extend(arr3)
    # print(bits)
    
    # Begin SPI transaction
    bus.write_byte_data(address, 0x03, 0xFE) # Write SCK low, rest high
    if cs == 0:
        bus.write_byte_data(address, 0x02, 0x7F) # CS0
    elif cs == 1:
        bus.write_byte_data(address, 0x02, 0xBF) # CS1
    elif cs == 2:
        bus.write_byte_data(address, 0x02, 0xDF) # CS2
    else:
        print("Invalid CS value")
            
    # bus.write_byte_data(address, 0x02, 0xBF) # CS1

    # Step through 48-bit SPI transaction
    for x in bits:
        if x==1:
            bus.write_byte_data(address, 0x03, 0xFE)
            bus.write_byte_data(address, 0x03, 0xFF)
            bus.write_byte_data(address, 0x03, 0xFF)
            bus.write_byte_data(address, 0x03, 0xFE)
        elif x==0:
            bus.write_byte_data(address, 0x03, 0xFA)
            bus.write_byte_data(address, 0x03, 0xFB)
            bus.write_byte_data(address, 0x03, 0xFB)
            bus.write_byte_data(address, 0x03, 0xFA)
    
    # End SPI transaction
    bus.write_byte_data(address, 0x02, 0xFF)

def read_gspi(addr, cs):
    arr1 = bin_array(READ_CW)
    arr2 = bin_array(addr)
    bits = []
    bits.extend(arr1)
    bits.extend(arr2)
    # print(bits)
    
    # Begin SPI transaction
    bus.write_byte_data(address, 0x03, 0xFE) # Write SCK low, rest high
    if cs == 0:
        bus.write_byte_data(address, 0x02, 0x7F) # CS0
    elif cs == 1:
        bus.write_byte_data(address, 0x02, 0xBF) # CS1
    elif cs == 2:
        bus.write_byte_data(address, 0x02, 0xDF) # CS2
    else:
        print("Invalid CS value")
           
    # bus.write_byte_data(address, 0x02, 0xBF) # CS1

    # Step through 48-bit SPI transaction
    for x in bits:
        if x==1:
            bus.write_byte_data(address, 0x03, 0xFE)
            bus.write_byte_data(address, 0x03, 0xFF)
            bus.write_byte_data(address, 0x03, 0xFF)
            bus.write_byte_data(address, 0x03, 0xFE)
        elif x==0:
            bus.write_byte_data(address, 0x03, 0xFA)
            bus.write_byte_data(address, 0x03, 0xFB)
            bus.write_byte_data(address, 0x03, 0xFB)
            bus.write_byte_data(address, 0x03, 0xFA)
    
    out_array = []
    # Read 16 Bits off the MISO line
    for i in range(16):
        bus.write_byte_data(address, 0x03, 0xFB)
        return_byte = bus.read_byte_data(address,0x01)
        return_bit = (return_byte >> 1) & 0x1
        out_array.append(return_bit)
        bus.write_byte_data(address, 0x03, 0xFA)
    
    # End SPI transaction
    bus.write_byte_data(address, 0x02, 0xFF)

    value = unarray_bin(out_array)
    return(value)

def auto_inc_read(addr, cs, length):
    arr1 = bin_array(AUTO_INC_CW)
    arr2 = bin_array(addr)
    bits = []
    bits.extend(arr1)
    bits.extend(arr2)
    output_list = []
    # print(bits)
    
    # Begin SPI transaction
    bus.write_byte_data(address, 0x03, 0xFE) # Write SCK low, rest high
    if cs == 0:
        bus.write_byte_data(address, 0x02, 0x7F) # CS0
    elif cs == 1:
        bus.write_byte_data(address, 0x02, 0xBF) # CS1
    elif cs == 2:
        bus.write_byte_data(address, 0x02, 0xDF) # CS2
    else:
        print("Invalid CS value")
           
    # bus.write_byte_data(address, 0x02, 0xBF) # CS1

    # Step through 48-bit SPI transaction
    for x in bits:
        if x==1:
            bus.write_byte_data(address, 0x03, 0xFE)
            bus.write_byte_data(address, 0x03, 0xFF)
            bus.write_byte_data(address, 0x03, 0xFF)
            bus.write_byte_data(address, 0x03, 0xFE)
        elif x==0:
            bus.write_byte_data(address, 0x03, 0xFA)
            bus.write_byte_data(address, 0x03, 0xFB)
            bus.write_byte_data(address, 0x03, 0xFB)
            bus.write_byte_data(address, 0x03, 0xFA)
    
    for j in range(length):
        out_array = []
        # Read 16 Bits off the MISO line
        for i in range(16):
            bus.write_byte_data(address, 0x03, 0xFB)
            return_byte = bus.read_byte_data(address,0x01)
            return_bit = (return_byte >> 1) & 0x1
            out_array.append(return_bit)
            bus.write_byte_data(address, 0x03, 0xFA)
        value = unarray_bin(out_array)
        output_list.append(value)
    
    # End SPI transaction
    bus.write_byte_data(address, 0x02, 0xFF)
    return output_list
    


# This is to read the GPIO pins on port 0
data = bus.read_byte_data(address,0x00)
print("Data on port 0")
print(data)

# Configure I/O for input or output
bus.write_byte_data(address, 0x06, 0x1F)
bus.write_byte_data(address, 0x07, 0xFA)

# Write to EYE_MON_INT_CFG_3 per sec 4.9.12.1
send_gspi(0x0057, 0x8006, 1)
send_gspi(0x0057, 0x8006, 2)

time.sleep(1)

# Disable Bus-Through Operation on All GSPI chips
send_gspi(0x0000, 0x2000, 0)
send_gspi(0x0000, 0x2000, 1)
send_gspi(0x0000, 0x2000, 2)

# Configure the Eye Monitor Vertical and Phase Offsets
# send_gspi(0x005a, 0x007f, 1) # 007f is the default horizontal offset and is required
# send_gspi(0x005b, 0x0000, 1) # 00 is default and required, 04 reduces test time by 1/4
# send_gspi(0x005c, 0xff00, 1) # ff is default and required, 04 reduces test time by 1/4

# Rest for a second
time.sleep(1)

send_gspi(0x005D, 0x0000, 1)

# Turn on eye monitor
send_gspi(0x005D, 0x0003, 1)
# Wait 5 seconds
time.sleep(5)
# Read status (Data is in status)
status = read_gspi(0x0090, 1)

# Read rate detected by GS12341
data = read_gspi(0x0087, 1)
print("Rate detected by GS12341 is", data)

# Get Data
for i in range(256): # Read 256 vertical lines
    counter = 0
    while((status & 0x3 == 0) or (status & 0x3 == 1)):
        time.sleep(0.1) # Wait 1 second before re-reading status
        status = read_gspi(0x0090, 1)
        counter = counter + 1
        if counter == 10:
            send_gspi(0x005D, 0x0003, 1)
            counter = 0
            print("Restarting eye monitor because status 0 or 1")
    if(status & 0x3 == 3):
        print("Aborted!")
        break
    elif(status & 0x3 == 2):
        eye_row = []
        counter = 0
        time.sleep(0.1)
        length_raw = read_gspi(REG_OFFSET + 1, 1)
        length = int((length_raw-4)/2)
        print(length)
        eye_row = auto_inc_read(REG_OFFSET + 2, 1, length)    
        eye_data.append(eye_row)

        time.sleep(0.1)
        
        # Reset Eye Scanner
        send_gspi(0x005D, 0x0002, 1)
        
        time.sleep(0.1)

        while(status & 0x3 != 0):
            status = read_gspi(0x0090, 1)
            time.sleep(0.1)
            counter = counter + 1
            if counter == 10:
                send_gspi(0x005D, 0x0002, 1)
        
        # Turn the Eye Monitor back on
        send_gspi(0x005D, 0x0003, 1)

send_gspi(0x005D, 0x0000, 1)

# All the information is in eye_data 
# Clean up data
for i in range(len(eye_data)):
    for j in range(len(eye_data[i])):
        if eye_data[i][j] > 2000:
            eye_data[i][j] = 2000

print(eye_data)

plt.imshow(eye_data)
plt.show()