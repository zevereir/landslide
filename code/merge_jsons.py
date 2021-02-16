import json
from pathlib import Path
import os
# new_dict={}
# path=Path("D://Thesis//landslide//data//Annotations//results")
# for i in os.listdir(path):
#     with open(path/i) as fp:
#         annotations=json.load(fp)
#     for x in annotations:
#         if "Done" in annotations[x]["file_attributes"] and annotations[x]["file_attributes"]["Done"]=="Yes":
#             new_dict[x]=annotations[x]
#         # elif int(x[:x.find("_")])<501:
#         #     print(x[:x.find("_")])
# print(len(new_dict))
# with open(path/"full_annotation.json","w") as j :
#     json.dump(new_dict,j)
path=Path("D://Thesis//landslide//data//Annotations//results//full3.json")
new_dict={}
with open(path) as fp:
    dict = json.load(fp)
count={}
for x in dict:
    if "Slide type" in dict[x]["file_attributes"]:
        z=dict[x]["file_attributes"]["Slide type"]
        if z in ["Objects in scope & equal to archetype","Objects in scope & superset o f archetype"]:
            new_dict[x]=dict[x]
        if z in count:
            count[z]+=1
        else:
            count[z]=1
    elif "kopie" not in x:
        print(x[:x.find("_")])
print(len(new_dict))
with open("D://Thesis//landslide//data//Annotations//results//experiments.json","w") as st:
    json.dump(new_dict,st)
for i in count:
    print(i+":",count[i])
print("Total: ",sum(count.values()))