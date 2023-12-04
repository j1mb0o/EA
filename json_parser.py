import json
import os
import shutil

# JSON string

file_path = 'results.json'

with open(file_path, 'r') as f:
    data = json.load(f)

# print(data[0])
names = []
for i in data[:5]:
    temp = []
    for j in i[1]:
        if type(j) == int:
            temp.append(str(j))
        else:
            temp.append(j)
    
    names.append(temp)

final_names = []
for i in names:
    # print('_'.join(i))
    final_names.append('_'.join(i))

for i in final_names:
    print(i)

for dir in os.listdir('data'):
    # print(dir)
    with open('data/' + dir + '/IOHprofiler_f18_LABS.json', 'r') as f:
        data = json.load(f)
        # print(data['algorithm']['name'])
        name = data['algorithm']['name']
        if name in final_names:
            shutil.make_archive('data/' + dir, 'zip', 'data/' + dir)
            print(dir)
            # exit()

