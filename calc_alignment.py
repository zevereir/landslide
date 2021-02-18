import json
import matplotlib.pyplot as plt
def check_rules(alignment,elements,repr, element):
    if len(elements)==0 or alignment=="TITLE":
        return True
    else:
        if alignment in ["LEFTSUBTITLE","MIDDLESUBTITLE","LEFTCONTENT","MIDDLECONTENT"]:
            for ele in elements:
                if ele[1]=="RIGHTCONTENT" or ele[1]=="RIGHTSUBTITLE":
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  not in ["b","m","o","s","eq"]:

                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  not in ["d","f","eq"]:

                                    return False
        if alignment in ["RIGHTSUBTITLE,MIDDLESUBTITLE","RIGHTCONTENT","MIDDLECONTENT"]:
            for ele in elements:
                if ele[1]=="LEFTCONTENT" or ele[1]=="LEFTSUBTITLE":
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  in ["b","m","o","s"]:

                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  in ["d","f"]:

                                    return False

        if "SUBTITLE" in alignment:
            for ele in elements:
                if "CONTENT" in ele[1]:
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  in ["b","m","o","s"]:

                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  in ["d","f"]:

                                    return False
        if "CONTENT" in alignment:
            for ele in elements:
                if "SUBTITLE" in ele[1]:
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  not in ["b","m","o","s","eq"]:

                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  not in ["d","f","eq"]:

                                    return False
        return True
import os
from pathlib import Path
with open("D://Thesis//landslide//data//Annotations//alignments.json") as ali:
    alignments=json.load(ali)
with open("D://Thesis//landslide//data//Annotations//results//annotated_data//roles.json") as rp:
    roles=json.load(rp)
res_path=Path("D:/Thesis/landslide/data/Annotations/results/annotated_data/results/results")
resulting=[]
confidence=[]
for file in os.listdir(res_path):
    with open(res_path/file) as fp:
        results=json.load(fp)
        total_score=0
        total_resp=0
        total_comp=0
        for slide_id in range(1,len(results)+1):
            #print("----------------------------")
            slide=results[str(slide_id)]
            slide_roles=roles[str(slide_id)]
            total_comp+=slide["Comparisons"]
            arch=slide["Archetype"]
            mapping=slide["Best mapping"]
            role_mapping=slide["Best role mapping"]
            #print("Responsitivity",slide["Responsitivity"])
            total_resp+=slide["Responsitivity"]
            #print("Arch",arch)
            #print("Mapping",mapping)
            #print("role_mapping",role_mapping)
            #print("Slide roles",slide_roles)
            if arch<9:
                pass
                #print("Alignments",alignments[str(arch)])
            score=0
            #print("Slide = ",slide["New slide"])
            #print("Archetype = ",slide["Archetype representation"])
            #print("MAPPINGS")
            current_mappings=set()
            new_slide=slide["New slide"]
            arch_repr=slide["Archetype representation"]
            slide_repr={x for x in new_slide[11:-2].split(", ")}
            #print(slide_repr)
            for element in range(0,len(slide_roles)):
                if str(element) in mapping:
                    if str(-mapping[str(element)]) in role_mapping:
                        #print(slide_roles[element] +"--> "+role_mapping[str(-mapping[str(element)])].upper())
                        rule=check_rules(role_mapping[str(-mapping[str(element)])].upper(),current_mappings,slide_repr,element)

                        if slide_roles[element] in alignments[str(arch)][role_mapping[str(-mapping[str(element)])].upper()] and rule:
                            score+=1
                        current_mappings.add((element,role_mapping[str(-mapping[str(element)])].upper()))

            if "background" in new_slide and "background" in arch_repr:
                ind1=new_slide[new_slide.find("background")+11:new_slide.find("background")+12]
                ind2=arch_repr[arch_repr.find("background")+11:arch_repr.find("background")+12]
                if ind1 in mapping and mapping[ind1]==-int(ind2):
                    score+=1
            if len(mapping)==0:
                total_score+=1
                #print(1.0)
            else:
                #print(score/max(1,len(mapping)))
                total_score+=(score/max(1,len(mapping)))
        resulting.append((file,total_resp/409,total_score/409,total_comp))

# baseline=[]
# learned=[]
# masters=[]
# for res in resulting:

#     if res[0].startswith("greedy"):
#         amount=int(res[0].replace("_False.json","")[res[0].find("_0_")+3:])
#         print(res[0][11:res[0].find("_0_")],amount,res[3])
#         if "learned" in res[0]:
#             learned.append((res[3],res[1],res[2]))
#         elif "baseline" in res[0]:
#             baseline.append((res[3],res[1],res[2]))
#         elif "masters" in res[0]:
#
#             masters.append((res[3],res[1],res[2]))
#
# baseline.sort()
# masters.sort()
# learned.sort()
# for ix in range(0,3):
#     i=[baseline,learned,masters][ix]
#     name=["baseline","learned","masters"][ix]
#     x_val=[]
#     y_val=[]
#     z_val=[]
#     for x in i:
#         x_val.append(x[0])
#         y_val.append(x[1])
#         z_val.append(x[2])
#     plt.plot(x_val,y_val,linestyle="solid",label="Resp "+name)
#     plt.plot(x_val,z_val,linestyle="dotted",label="Sens "+name)
baseline={}
learned={}
masters={}

for res in resulting:
    if res[0].startswith("greedy"):
        if "learned" in res[0]:
            if res[3] in learned:
                learned[res[3]].append((res[1],res[2]))
            else:
                learned[res[3]]=[(res[1],res[2])]
        elif "baseline" in res[0]:
            if res[3] in baseline:
                baseline[res[3]].append((res[1],res[2]))
            else:
                baseline[res[3]]=[(res[1],res[2])]
        elif "masters" in res[0]:
            if res[3] in masters:
                masters[res[3]].append((res[1],res[2]))
            else:
                masters[res[3]]=[(res[1],res[2])]
new_baseline=[]
new_learned=[]
new_masters=[]
#
for v in masters:
    z=masters[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    new_masters.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens)))
for v in baseline:
    z=baseline[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    new_baseline.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens)))
for v in learned:
    z=learned[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    new_learned.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens)))
#
new_learned.sort()
new_masters.sort()
new_baseline.sort()

for ix in range(0,3):
    i=[new_baseline,new_learned,new_masters][ix]
    name=["baseline","learned","masters"][ix]
    lcolor=["g","r","b"][ix]

    x_val=[p[0] for p in i]

    resp_min=[p[1] for p in i]
    resp_mean=[p[2] for p in i]
    resp_max=[p[3] for p in i]
    sens_min=[p[4] for p in i]
    sens_mean=[p[5] for p in i]
    sens_max=[p[6] for p in i]

    print([x/(10**7)  for x in x_val])
    plt.plot(x_val,resp_min,lcolor,linestyle="solid",label="Resp "+name)
    plt.plot(x_val,sens_min,lcolor,linestyle="dotted",label="Sens "+name)

plt.legend()
plt.show()





# import json
# import xml.etree.ElementTree as ET
# dict={}
# tree= ET.parse("D://Thesis//landslide//data//Annotations//results//annotated_data//annotated_categorized.xml")
#
# counter=1
# for page in tree.getroot():
#     roles=[]
#     for element in page:
#         roles.append(element.attrib.get("Role"))
#     dict[str(counter)]=roles
#     counter+=1
# with open("D://Thesis//landslide//data//Annotations//results//annotated_data//roles.json","w") as rl:
#     json.dump(dict,rl)
#
