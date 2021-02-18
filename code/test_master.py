import json


def findLargestNumber(text):
    return max(map(int,list(''.join(i for i in text if i.isdigit()))))
count=0
other_count=0
with open("D://Thesis//landslide//code//archetypes//masters.json") as jp:
    archetypes=json.load(jp)

for i in list(archetypes.keys()):
    masters=archetypes[i]
    for repri in masters.values():
        for repr in repri:
            biggest=findLargestNumber(str(repr["Representation"]))
            mapping=len(repr["Mapping"])
            if biggest+1!=mapping and "background" not in str(repr["Representation"]):
                print(str(repr["Representation"]))
                print(repr["Mapping"])
                count+=1
            else:
                other_count+=1
print("Total Count",count, other_count)