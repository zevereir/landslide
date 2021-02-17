import json

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
                                    print("WRONGG")
                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  not in ["d","f","eq"]:
                                    print("WRONGG")
                                    return False
        if alignment in ["RIGHTSUBTITLE,MIDDLESUBTITLE","RIGHTCONTENT","MIDDLECONTENT"]:
            for ele in elements:
                if ele[1]=="LEFTCONTENT" or ele[1]=="LEFTSUBTITLE":
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  in ["b","m","o","s"]:
                                    print("WRONGG")
                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  in ["d","f"]:
                                    print("WRONGG")
                                    return False

        if "SUBTITLE" in alignment:
            for ele in elements:
                if "CONTENT" in ele[1]:
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  in ["b","m","o","s"]:
                                    print("WRONGG")
                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  in ["d","f"]:
                                    print("WRONGG")
                                    return False
        if "CONTENT" in alignment:
            for ele in elements:
                if "SUBTITLE" in ele[1]:
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  not in ["b","m","o","s","eq"]:
                                    print("WRONGG")
                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  not in ["d","f","eq"]:
                                    print("WRONGG")
                                    return False
        return True

rules_counter=0
with open("D://Thesis//landslide//data//Annotations//alignments.json") as ali:
    alignments=json.load(ali)
with open("D://Thesis//landslide//data//Annotations//results//annotated_data//results//greedy_all_masters_0_10000_False.json") as fp:
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
            print("Slide roles",slide_roles)
            if arch<9:
                pass
                print("Alignments",alignments[str(arch)])
            score=0
            print("Slide = ",slide["New slide"])
            print("Archetype = ",slide["Archetype representation"])
            print("MAPPINGS")
            current_mappings=set()
            new_slide=slide["New slide"]
            arch_repr=slide["Archetype representation"]
            slide_repr={x for x in new_slide[11:-2].split(", ")}
            print(slide_repr)
            for element in range(0,len(slide_roles)):
                if str(element) in mapping:
                    if str(-mapping[str(element)]) in role_mapping:
                        print(slide_roles[element] +"--> "+role_mapping[str(-mapping[str(element)])].upper())
                        rule=check_rules(role_mapping[str(-mapping[str(element)])].upper(),current_mappings,slide_repr,element)
                        if not rule:
                            rules_counter+=1
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
                print(1.0)
            else:
                print(score/max(1,len(mapping)))
                total_score+=(score/max(1,len(mapping)))
print("TOTAL RESP",total_resp/len(results))
print("TOTAL SCORE",total_score/len(results))
print("RULES EFFECT",rules_counter)





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
