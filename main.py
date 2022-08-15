import numpy as np
data = np.loadtxt('info.csv',unpack = True, usecols=(1,2,3), dtype = str, delimiter= ",")
# def clean_info(list):
    
#     string = ''.join(string.split(' '))  #remove spaces

    
matching_to = np.loadtxt('matches.csv',unpack = True,usecols=(0,1,2,3,4,5,6), dtype = str, delimiter= ",")
#0 is first match
#1 is second match
#2 is second match num
# matching_number = dict(zip(info[1,1::],info[2,1::]))
def direct_matches(a,b):
    x = list(set(a).intersection(set(b)))
    return x
def indirect_matches(a,b):
    a = b
matched_items = np.array(direct_matches(data[0],data[1])); matched_items = sorted(matched_items)
matched_items = np.hstack((matched_items,np.zeros((len(matched_items)), dtype = np.int32)))
matched_items = np.reshape(matched_items, (-1, 2), order = 'F')
index = 0
while index < matched_items.shape[0]:
    i = matched_items[index,0]
    val = np.where(data[1] == i)[0]
    # print(i,val)
    if len(val) > 1:
        for ind, vals in enumerate(val):
            if ind == 0:
                matched_items[index, 1] =  data[2,vals]
            else:
                matched_items = np.insert(matched_items,index+ind-1, [i,data[2,vals]], axis = 0)
        index+=ind+1
    else:
        val = int(val)
        matched_items[index, 1] =  data[2,val]
        index +=1
for i in range(matching_to.shape[1]):
    matching_to[5,i] = ''
    matching_to[6,i] = ''


temp_dict = {}
for index, i in enumerate(matched_items):
    if i[0] in temp_dict.keys():
        temp_dict[i[0]] += 1
        print(i)
    else:
        temp_dict[i[0]] = 0
    
    val = np.where(matching_to[2] == i[0])[0]
    if len(val) > 1:
        try:
            val = val[temp_dict[i[0]]]
        except:
            pass
    else:
        val = int(val)
    matching_to[5][val] = i[0]
    matching_to[6][val] = i[1]
x = 0
    # matched_items[index, 1] =  data[2,val]
    
# (array([ 1411,  1809,  2532,  4133,  7029, 10308, 15398]),) 
# for index, i in enumerate(matched_items):
    # print(np.where(matches[2] == i), "\n")
import csv
with open('example.csv', 'w') as file:
    writer = csv.writer(file)
    for i in range(matching_to.shape[1]):
        writer.writerow(matching_to[:,i])
x=0