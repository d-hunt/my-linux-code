import numpy as np
import matplotlib.pyplot as plt
import ast

eye_data = []

filename = 'eye_data_bypass_eq_fullres.txt'

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

plt.imshow(eye_data)
plt.show()