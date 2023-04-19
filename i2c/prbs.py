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


# Write to EYE_MON_INT_CFG3 for some reason?
send_gspi(0x0057, 0x8006, 1)
send_gspi(0x0057, 0x8006, 2)

time.sleep(1)

# Disable Bus-Through Operation on All GSPI chips
send_gspi(0x0000, 0x2000, 0)
send_gspi(0x0000, 0x2000, 1)
send_gspi(0x0000, 0x2000, 2)

time.sleep(1)

# Configure GS12281 for PRBS Generation
send_gspi(0x0048, 0x0003, 2)    # Signal select
time.sleep(1)
send_gspi(0x0003, 0x0000, 2)    # Disable sleep
time.sleep(1)
send_gspi(0x0049, 0x0000, 2)    # Disable Mute
time.sleep(1)
send_gspi(0x004A, 0x0000, 2)    # Disable Auto-Disable (Disabled by Default)
time.sleep(1)
send_gspi(0x004B, 0x0404, 2)    # Slew Control
time.sleep(1)
send_gspi(0x0052, 0x0106, 2)    # Configure PRBS parameters
print("Starting Generator")
send_gspi(0x0052, 0x0306, 2)   
time.sleep(10)


# Start Generator

# Configure GS12341 for PRBS Checking
send_gspi(0x0050, 0x0899, 1)    # Set time to 1s
# Disable Sleep mode on GS12341
send_gspi(0x0003, 0x0000, 1)
# Initiate PRBS Check
send_gspi(0x0051, 0x0101, 1)    # Initiate Timed PRBS Check
time.sleep(2)
count = 0
checking = 1

while(checking):
    # Read PRBS Status
    status = read_gspi(0x008A, 1)
    time.sleep(1)
    print("Status:",status)

    if(status&0x3) == 0x0:
        send_gspi(0x0051, 0x0100, 1) # Stop checker
        while status == 256 or status == 259:
            count = count + 1
            status = read_gspi(0x008A,1)
            time.sleep(1)
            if (count == 10):
                print("Aborted in status check")
                break
        send_gspi(0x0051, 0x0100, 1) # Restart checker
        print("Starting Checker")
        time.sleep(1)

    if(status&0x3) == 0x3:
        print("Bad Checker")
        send_gspi(0x0051, 0x0100, 1) # Stop checker
        while status == 256 or status == 259:
            count = count + 1
            status = read_gspi(0x008A,1)
            time.sleep(1)
            if (count == 10):
                print("Aborted in status check")
                break
        count = count + 1
        if(count >= 5):
            print("Aborted")
            break
        send_gspi(0x0051, 0x0100, 1) # Stop checker
        send_gspi(0x0052, 0x0106, 2)  # Stop Generator
        print("Stopping Checker")
        time.sleep(1)
        status = read_gspi(0x008A, 1)
        print("Status:",status)

        while(status&0x3) != 0x0:
            time.sleep(1)
            status = read_gspi(0x008A, 1)
            print("Status:",status)

        send_gspi(0x0052, 0x0306, 2) # Restart Generator
        send_gspi(0x0051, 0x0101, 1) # Restart checker
        print("Starting Checker")
        time.sleep(1)

    elif(status&0x3)== 0x1:
        print("Waiting...")
        time.sleep(1)

    elif(status&0x3)== 0x2:
        checking = 0

num_errors = read_gspi(0x0089, 1)
print(num_errors)