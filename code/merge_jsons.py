import json
from pathlib import Path
import os
new_dict={}
path=Path("D://Thesis//landslide//data//Annotations//results//annotated_data//results")
count=1
exp="greedy_all_baseline_0_40000_False_"
for i in os.listdir(path):
    if exp in i:
        with open(path/i) as fp:
            results=json.load(fp)
            print(len(results))
        for i in results:
            new_dict[count]=results[i]
            count+=1
print(len(new_dict))
with open(path/(exp[:-1]+".json"),"w") as j :
    json.dump(new_dict,j)
