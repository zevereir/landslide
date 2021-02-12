import json
from pathlib import Path
import os
new_dict={}
path=Path("D://Thesis//landslide//data//Annotations//results")
for i in os.listdir(path):

    with open(path/i) as fp:
        annotations=json.load(fp)
    for x in annotations:
        if "Done" in annotations[x]["file_attributes"] and annotations[x]["file_attributes"]["Done"]=="Yes":
            new_dict[x]=annotations[x]
print(len(new_dict))
with open(path/"full_annotation.json","w") as j :
    json.dump(new_dict,j)
