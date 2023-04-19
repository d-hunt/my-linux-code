import numpy
import matplotlib.pyplot as plt

a = [1,1,1,1,1,1,1,1,1,1]
b = [1,1,1,1,0,0,0,0,0,1]
c = [0,0,0,0,0,0,0,0,0,0]
d = [1,1,1,1,0,0,0,0,0,1]
e = [1,1,1,1,1,1,1,1,1,1]
f=[]
f.append(a)
f.append(b)
f.append(c)
f.append(d)
f.append(e)

# find the rows with the most ones
def center_eye(f):
    row_count = [0]*len(f[0])
    print(row_count)
    for i in range(len(f)):
        for j in range(len(f[i])):
            if f[i][j] == 1:
                row_count[j] = row_count[j] + 1
    print(row_count)

    block_list = []
    for i in range(len(row_count)):
        if row_count[i] != max(row_count):
            block_list.append(row_count[i])

    shift = int(sum(block_list)/len(block_list))

    output_list =[]
    for i in range(len(f)):
        row_buffer=[]
        for j in range(shift, len(f[i])):
            row_buffer.append(f[i][j])
        for j in range(0, shift):
            row_buffer.append(f[i][j])
        output_list.append(row_buffer)
    return output_list
plt.imshow(output_list)
plt.show()