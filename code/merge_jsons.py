import json
from pathlib import Path
import os
new_dict={}
path=Path("D://Thesis//landslide//data//Annotations//results//annotated_data//results")
count=1
exp="greedy_all_masters_0_15000_False_"
partitions=[x for x in os.listdir(path) if exp in x and "-32" in x]
print(len(partitions))
for ind in range(1,len(partitions)+1):
    i=[z for z in partitions if "_"+str(ind)+"-" in z][0]
    with open(path/i) as fp:
        results=json.load(fp)
        print(len(results))
    for i in results:
        new_dict[count]=results[i]
        count+=1
print(len(new_dict))
with open(path/"results"/(exp[:-1]+".json"),"w") as j :
    json.dump(new_dict,j)
