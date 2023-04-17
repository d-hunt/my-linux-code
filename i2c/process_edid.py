with open('edid.txt', 'r') as f:
    data = eval(f.read())

hex_list = [hex(x)[2:].zfill(4) for x in data]


with open('edid_hex.txt', 'w') as f:
    for hex_value in hex_list:
        f.write(hex_value + '\n')

