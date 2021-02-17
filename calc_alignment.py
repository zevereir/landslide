import json
with open("D://Thesis//landslide//data//Annotations//alignments.json") as ali:
    alignments=json.load(ali)
with open("D://Thesis//landslide//data//Annotations//results//annotated_data//results//greedy_all_baseline_0_20000_False.json") as fp:
    results=json.load(fp)
    with open("D://Thesis//landslide//data//Annotations//results//annotated_data//roles.json") as rp:
        roles=json.load(rp)
        total_score=0
        total_resp=0
        for slide_id in range(1,len(results)+1):
            print("----------------------------")
            slide=results[str(slide_id)]
            slide_roles=roles[str(slide_id)]
            arch=slide["Archetype"]
            mapping=slide["Best mapping"]
            role_mapping=slide["Best role mapping"]
            print("Responsitivity",slide["Responsitivity"])
            total_resp+=slide["Responsitivity"]
            #print("Arch",arch)
            print("Mapping",mapping)
            print("role_mapping",role_mapping)
            #print("Slide roles",slide_roles)
            if arch<9:
                pass
                print("Alignments",alignments[str(arch)])
            score=0
            print("Slide = ",slide["New slide"])
            print("Archetype = ",slide["Archetype representation"])
            print("MAPPINGS")
            for element in range(0,len(slide_roles)):
                if str(element) in mapping:
                    if str(-mapping[str(element)]) in role_mapping:
                        print(slide_roles[element] +"--> "+role_mapping[str(-mapping[str(element)])].upper())
                        if slide_roles[element] in alignments[str(arch)][role_mapping[str(-mapping[str(element)])].upper()]:
                            score+=1
            new_slide=slide["New slide"]
            arch_repr=slide["Archetype representation"]
            if "background" in new_slide and "background" in arch_repr:
                ind1=new_slide[new_slide.find("background")+11:new_slide.find("background")+12]
                ind2=arch_repr[arch_repr.find("background")+11:arch_repr.find("background")+12]
                if ind1 in mapping and mapping[ind1]==-int(ind2):
                    score+=1
            if len(mapping)==0:
                total_score+=1
                print(1.0)
            else:
                print(score/max(1,len(mapping)))
                total_score+=(score/max(1,len(mapping)))
print("TOTAL SCORE",total_score/len(results))
print("TOTAL RESP",total_resp/len(results))





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
