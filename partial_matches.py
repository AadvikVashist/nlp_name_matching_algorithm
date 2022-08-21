import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import time
import csv 
import sys
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
#
#
save_location = "saved.csv"
#
#
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
pick_up = input("pick up where you left off?")
if pick_up == "yes" or "y" in pick_up:
    pick_up = True
    print("picking up where you left off.....")
    try:
        csv_file_array = np.array(pd.read_csv(save_location, sep = ","))
    except:
        csv_file_array = np.array([[]])
    csvfileobj = open(save_location, mode = "a+", newline='')
    curr_index = 0
else:
    inputs = input("are you sure?")
    if inputs == "yes" or "y" in inputs:
        pick_up = False
        print("okay then, lets start from square one :irritated")
        csvfileobj = open(save_location, mode = "w", newline='')
    else:
        pick_up = True
        curr_index = 0
csvfileobject = csv.writer(csvfileobj)
for index, value in enumerate(ordered_2015):
    if pick_up:
        a = np.where(csv_file_array[:,2] == value[2])
        # b = [val for val in a[:,2] if val!=None]
        if  a[0].shape != (0,):
            csv_index = 0
            for i in a:
                if i[0] > curr_index:
                    csv_index= i
                    break
            curr_index = i
        if curr_index == (csv_file_array.shape)[0]-1:
            pick_up = False
        # continue
        #     curr_index =index
    else:
        try:
            curr_matched = [(index, x, *match(value[2], x)) for index,x in enumerate(dict_2010[value[0]][:,2])]
        except:
            curr_matched = [(index, x, *match(value[2], x)) for index,x in enumerate(ordered_2010[:,2])]            
        curr_matched = sorted(curr_matched, key=lambda x: x[2])
        index_of_max_in_2010 = 0 #np.argmax(np.array(curr_matched)[:,2])
        index_of_2010_match = curr_matched[index_of_max_in_2010][0]
                
            # index_of_2010_match = np.argmax()
            # indexes = np.argpartition([match(value[2], x)[0] for x in dict_2010[value[0]][:,2]], -10)[-10:]
            # multi_matches = dict_2010[value[0]][indexes,2]
            # if index_of_2010_match not in multi_matches:
            #   
            # assert False, ("bad")
        match_percentage = curr_matched[index_of_max_in_2010][2::]
        if np.mean(match_percentage) > 0.8: 
            value = list(value)
            value.extend(dict_2010[value[0]][curr_matched[index_of_max_in_2010][0]])
            value.extend(match_percentage)
            matched_list.append(value)
            csvfileobject.writerow(value)
            print(value)
        elif np.mean(match_percentage) > 0.3:
            # print(f"{value[2]} and {dict_2010[value[0]][index_of_2010_match][2]}? Match percentage is {match_percentage[0]*100}% | {match_percentage[1]*100}%" )
            while True:
                for i in range(5):
                    print(f"{i}:",f"{value[2]} and {curr_matched[i][1]} || {np.round(curr_matched[i][2]*100, 2)}% | {np.round(curr_matched[i][3]*100,2)}%" )
                inp = input("'enter' / ' ' or 1,2,3,4: ")
                inp = inp.lower()
                if "y" in inp or "0" in inp or inp == "":
                    value = list(value)
                    value.extend(dict_2010[value[0]][curr_matched[index_of_max_in_2010][0]])
                    value.extend(match_percentage)
                    matched_list.append(value)
                    csvfileobject.writerow(value)
                    break
                elif " " in set(inp.split())   or "n" in inp:
                    print("continuing to next......")
                    break
                elif "exit" in inp:
                    csvfileobj.close()
                    sys.exit("exiting.....")
                    break
                else:
                    try:
                        x = int(inp)
                        value = list(value)
                        value.extend(dict_2010[value[0]][curr_matched[x][0]])
                        value.extend(match_percentage)
                        matched_list.append(value)
                        csvfileobject.writerow(value)
                    except:
                        print("invalid input")
                        continue
        else:
            continue

# close the file
csvfileobj.close()
# district for both | block for 15 | gp for 15 | gp id for 15 | block for 10 if diff | 10 gp | 10 id
# print(fuzz.ratio('bighurd', 'boi ahurd')) #pattern mining library spmf sequential pattern mining algorithms | mitre identity matching | mitre challenge for identitiy matching | 