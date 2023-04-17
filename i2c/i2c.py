import smbus
import time

WRITE_CW = 0x2000
READ_CW = 0xA000

channel = 1
address = 0x20
bus = smbus.SMBus(channel)

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

def write_reg(addr, data, cs):
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
    time.sleep(0.015)
    # Step through 48-bit SPI transaction
    for x in bits:
        if x==1:
            bus.write_byte_data(address, 0x03, 0xFE)
            time.sleep(0.015)
            bus.write_byte_data(address, 0x03, 0xFF)
            time.sleep(0.015)
            bus.write_byte_data(address, 0x03, 0xFF)
            time.sleep(0.015)
            bus.write_byte_data(address, 0x03, 0xFE)
            time.sleep(0.015)
        elif x==0:
            bus.write_byte_data(address, 0x03, 0xFA)
            time.sleep(0.015)
            bus.write_byte_data(address, 0x03, 0xFB)
            time.sleep(0.015)
            bus.write_byte_data(address, 0x03, 0xFB)
            time.sleep(0.015)
            bus.write_byte_data(address, 0x03, 0xFA)
            time.sleep(0.015)
    
    # End SPI transaction
    bus.write_byte_data(address, 0x02, 0xFF)

def read_reg(addr, cs):
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

def send_spi(addr, data):
    arr2 = bin_array(addr)
    arr3 = bin_array(data)
    bits = []
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



# This is to read the GPIO pins on port 0
data = bus.read_byte_data(address,0x00)
print("Data on port 0")
print(data)

# Configure I/O for input or output
bus.write_byte_data(address, 0x06, 0x1F)
bus.write_byte_data(address, 0x07, 0xFA)


# Write to EYE_MON_INT_CFG3 for some reason?
write_reg(0x0057, 0x8006, 1)
write_reg(0x0057, 0x8006, 2)

time.sleep(1)

# Disable Bus-Through Operation on All GSPI chips
write_reg(0x0000, 0x2000, 0)
write_reg(0x0000, 0x2000, 1)
write_reg(0x0000, 0x2000, 2)

time.sleep(1)

# Configure GS212170
write_reg(0x007c,0x3668,0)
write_reg(0x00dc,0x0002,0)
write_reg(0x0098,0x0010,0)
write_reg(0x1065,0x0007,0)
write_reg(0x101B,0xDB6F,0)
write_reg(0x10f4,0x0001,0)
write_reg(0x10f8,0x0000,0)
write_reg(0x10fa,0x0000,0)
write_reg(0x10f9,0x0078,0)
write_reg(0x10f7,0x0810,0)
write_reg(0x10f5,0x0001,0)
write_reg(0x10f9,0x0078,0)
write_reg(0x10f7,0x0c10,0)
write_reg(0x10f5,0x0001,0)
write_reg(0x10f9,0x0078,0)
write_reg(0x10f7,0x1010,0)
write_reg(0x10f5,0x0001,0)
write_reg(0x10f9,0x0078,0)
write_reg(0x10f7,0x1410,0)
write_reg(0x10f5,0x0001,0)
write_reg(0x10f4,0x0000,0)
write_reg(0x10f9,0x0000,0)
write_reg(0x10f7,0x0000,0)
write_reg(0x1067,0x050d,0)
write_reg(0x1079,0x4239,0)
write_reg(0x1082,0x4239,0)
write_reg(0x1084,0x5fff,0)
write_reg(0x1085,0x5fff,0)
write_reg(0x1091,0x4239,0)
write_reg(0x1093,0x4a39,0)
write_reg(0x1065,0x0006,0)
write_reg(0x7069,0x0187,0) 

# Might need to add code for Bit Clock Scrambling

time.sleep(1)

# Do SCDC stuff
write_reg(0x006E, 0x00B0, 0) # Write 0x00B0 to STAT_SEL_A, which assigns the HDMI_TX_TMDS_CLK_RATIO to STAT0
write_reg(0x0072, 0x001F, 0) # Enables STAT outputs on STAT0-STAT4
write_reg(0x7002, 0x0003, 0) # Enabled HPD override with bit 1.  bit 2 overrides the HPD signal
write_reg(0x201D, 0x000F, 0) # Sets all 4 Tx in Idle state
write_reg(0x201E, 0x000F, 0) # Enables Idle State on all 4 Tx outputs 
write_reg(0x7007, 0x0020, 0) # SCDC Register address to write data to as 0x20

# # Conditional upon reads from STAT balls For 12G input, I will hardcode 1/40 and scrambling
# data = bus.read_byte_data(address,0x01) # Read output on port 1
# if (data >> 7):
#     write_reg(0x7008, 0x0003, 0) # Set data to write to SCDC register 0x20 as 0x03
# else:
#     write_reg(0x7008, 0x0000, 0) # Set data to write to SCDC register 0x20 as 0x00

write_reg(0x7008, 0x0003, 0) # Set data to write to SCDC register 0x20 as 0x03
write_reg(0x7006, 0x0001, 0) # Start the SCDC write

time.sleep(0.1)

write_reg(0x201D, 0x0000, 0) # Unsets Tx Idle on outputs
write_reg(0x201E, 0x0000, 0) # Disables Tx Idle on outputs


# Read rate detected by GS12341
data = read_reg(0x0087, 1) & 0x7
print("Rate detected by GS12341 is", data)

# Read input lock detected by GS12170
data = read_reg(0x0003, 0)
print("Lock detected by GS12170 is", data)

# Data rate detected by GS12170
data = read_reg(0x0007, 0) & 0x3
print("Rate detected by GS12170 is", data)

# # Initiate EDID Read
# write_reg(0x7005, 0x0001, 0)
# time.sleep(3)
# data = read_reg(0x700A, 0)
# if((data >> 9) & 0x1):
#     print("EDID read completed")
# else:
#     print("EDID read not completed")

# if((data >>10) & 0x1):
#     print("No ACK when EDID read")


