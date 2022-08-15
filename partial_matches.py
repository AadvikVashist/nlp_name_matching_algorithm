import numpy as np
from fuzzywuzzy import fuzz
import time
csv_2010 = np.loadtxt('2010_Orphaned.csv',unpack = True, usecols=(0,1,2,3),dtype = str, delimiter= ",")
csv_2015 = np.loadtxt('2015_Orphaned.csv',unpack = True, usecols=(0,1,2,3),dtype = str, delimiter= ",")
standard = 1
partial = 0.04
token = 0.3
_set = 0.3
wratio = 0.6
""" BOTH ARRAYS ARE DISTRICT | BLOCK | GP | GPID"""
ordered_2010 = csv_2010[[2,0,1,3,]]; 
ordered_2010 = ordered_2010.transpose()[1::]
ordered_2015  = csv_2015[[3,1,2,0]]
ordered_2015 = ordered_2015.transpose()[1::]

def add(list: np.array):
    for index, i in enumerate(list):
        if len(i[0]) <= 2 or i[0] is None:
            if index != 0 and index != list.shape[0] -1 and list[index-1,0] == list[index+1,0]:
                list[index,0] = list[index+1,0]
            elif index == 0:
                list[index,0] = list[index+1,0]
            elif index == list.shape[0]-1:
                list[index,0] = list[index-1,0]
            else:
                raise ValueError("list value " + str(i) + " has no district")
            print(list[index,0])
    return list
ordered_2015 = add(ordered_2015)
ordered_2010 = add(ordered_2010)
#distric names
matched_list = []
matching_districts = set(ordered_2015[:,0]) & set(ordered_2010[:,0])
unmatched_districts = {2010: set(ordered_2010[:,0]) - matching_districts, 2015: set(ordered_2015[:,0]) - matching_districts}
dict_2010 = {}
for i in set(ordered_2010[1::,0]):
    dict_2010[i] = []
for value in ordered_2010:
    dict_2010[value[0]].append(value)
for value in dict_2010:
    dict_2010[value] = np.array(dict_2010[value])
def match(s1,s2):
    natural_ratio = fuzz.ratio(s1,s2)/100
    if natural_ratio >= 0.9:
        return natural_ratio, natural_ratio
    elif natural_ratio >= 0.5:
        letter_diff = abs(len(s1)-len(s2))
        avg_length = np.mean((len(s1),len(s2)))
        if letter_diff != 0:
            letter_cutback = letter_diff/avg_length
        else:
            letter_cutback = avg_length
        cum_ratio = natural_ratio- (letter_cutback)
        
        # try:
        #     cum_ratio = cum_ratio**(1/avg_length)
        # except:
        #     pass
        return cum_ratio, natural_ratio
    else:
        return 0, natural_ratio
for index, value in enumerate(ordered_2015):
    if value[0] in matching_districts:
        index_of_2010_match = np.argmax([match(value[2], x)[0] for x in dict_2010[value[0]][:,2]])
        indexes = np.argpartition([match(value[2], x)[0] for x in dict_2010[value[0]][:,2]], -5)[-10:]
        vals = dict_2010[value[0]][indexes,2]

        [match(value[2], x)[0] for x in dict_2010[value[0]][:,2]])z
        match_percentage = match(value[2], dict_2010[value[0]][index_of_2010_match][2])
        if np.mean(match_percentage) > 0.8: 
            value = list(value)
            value.extend(dict_2010[value[0]][index_of_2010_match])
            value.extend(match_percentage)
            matched_list.append(value)
        else:
            print(f"{value[2]} and {dict_2010[value[0]][index_of_2010_match][2]}? Match percentage is {match_percentage[0]*100}% | {match_percentage[1]*100}%" )
            inp = input("yes/no or 1,2,3,4,5: ")
            inp = inp.lower()
            if "y" in inp:
                value = list(value)
                value.extend(dict_2010[value[0]][index_of_2010_match])
                value.extend(match_percentage)
                matched_list.append(value)
# district for both | block for 15 | gp for 15 | gp id for 15 | block for 10 if diff | 10 gp | 10 id
print(fuzz.ratio('bighurd', 'boi ahurd')) #pattern mining library spmf sequential pattern mining algorithms | mitre identity matching | mitre challenge for identitiy matching | 