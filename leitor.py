my_list = []
my_list.append(range(10))
my_list.append(range(10,20))
my_list.append(range(20,30))
my_list.append(range(30,40))
my_list.append(range(40,50))
my_list.append(range(50,60))
my_list.append(range(70,80))

with open('sementes.txt', 'w') as f:
    for s in my_list:
        f.write(str(s))
        f.write('\n')
#
my_list = []
with open('sementes.txt', 'r') as f:
    for line in f:
        x = line.replace("[", "")
        x = x.replace("]", "")
        x = x.replace("\n", "")
        x = x.replace(",", " ")
        my_list.append(x)

all_lines = [[int(num) for num in line.split()] for line in my_list]
