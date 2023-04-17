my_list = [1, 2, 3, 4, 5]
with open('output.txt', 'w') as file:
    for item in my_list:
        file.write(str(item) + '\n')