import numpy as np
import matplotlib.pyplot as plt
import ast

eye_data = []

filename = '12G_6ft_eq_REV0.txt'

with open(filename, 'r') as file:
    lines = file.readlines()
for x in lines:
    x.strip()
    list_ = ast.literal_eval(x)
    eye_data.append(list_)


# Clean up data
for i in range(len(eye_data)):
    for j in range(len(eye_data[i])):
        if eye_data[i][j] > 2000:
            eye_data[i][j] = 2000

def center_eye(f):
    row_count = [0]*len(f[0])
 
    for i in range(len(f)):
        for j in range(len(f[i])):
            if f[i][j] == 2000:
                row_count[j] = row_count[j] + 1
 

    block_list = []
    for i in range(len(row_count)):
        if row_count[i] == max(row_count):
            block_list.append(i)
    print(block_list)

    shift = int(sum(block_list)/len(block_list))
    print(shift)
    output_list =[]
    for i in range(len(f)):
        row_buffer=[]
        for j in range(shift, len(f[i])):
            row_buffer.append(f[i][j])
        for j in range(0, shift):
            row_buffer.append(f[i][j])
        output_list.append(row_buffer)
    return output_list

# def center_eye(input_list):
#     block_list = list(range(0, len(input_list[0])))

#     for i in range(len(input_list)):
#         for j in range(len(input_list[i])):
#             if input_list[i][j] != 2000:
#                 if j in block_list: block_list.remove(j)

#     shift = int(sum(block_list)/len(block_list))

#     output_list =[]
#     for i in range(len(input_list)):
#         row_buffer=[]
#         for j in range(shift, len(input_list[i])):
#             row_buffer.append(input_list[i][j])
#         for j in range(0, shift):
#             row_buffer.append(input_list[i][j])
#         output_list.append(row_buffer)
#     return output_list

my_new_data = center_eye(eye_data)
#print(my_new_data)

#plt.imshow(eye_data)
plt.imshow(my_new_data)
plt.show()