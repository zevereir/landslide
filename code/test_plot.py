from tree2features import tree2features
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import latex
from matplotlib import rc
import seaborn as sns
import json
for i in range(1,631):
    print(i)
    tree=ET.parse("D://Thesis//landslide//data//Main//"+str(i)+"_data//"+str(i)+"_preparsed.xml")
    xml_file="D://Thesis//landslide//data//Main//"+str(i)+"_data//"+str(i)+".xml"
    output_directory="D://Thesis//landslide//data//Main//"+str(i)+"_data"
    tree2features(tree, xml_file,output_directory, True)

with open("D://Thesis//landslide//data//Annotations//results//experiments.json") as fp:
    experiments=json.load(fp)
new_dict={}
for experiment in experiments:
    splitted=experiment.split("_")
    print(splitted[0])
    slideshow=splitted[1]
    slide=splitted[2][:splitted[2].find(".")]
    print("D://Thesis//landslide//data//Main//"+slideshow+"_data//"+slideshow+"_categorized.xml")
    tree = ET.parse("D://Thesis//landslide//data//Main//"+slideshow+"_data//"+slideshow+"_categorized.xml")
    element_js={}
    for page in tree.getroot():
        if int(page.attrib.get("id"))==int(slide)+1:
            for ele in page:
                type=ele.tag
                if type!=None:
                    un_id=ele.attrib.get("unique_id")
                    if "[" in un_id:
                        un_ids=[int(x) for x in un_id[1:-1].replace("'","").split(",")]
                    else:
                        un_ids=[int(un_id)]
                    for i in un_ids:
                        element_js[i]=type
                    cap=ele.attrib.get("caption_ids")
                    if cap!=None:
                        print("CAP",cap)
                        if "[" in cap:
                            cap_ids=[int(x) for x in cap[1:-1].replace("'","").split(",")]
                        else:
                            cap_ids=int(cap)
                        for i in cap_ids:
                            element_js[i]="caption"
            break
        new_dict[experiment]=element_js
with open("D://Thesis//landslide//data//Annotations//results//annotated_data//types_categorized.json","w") as tpy:
    json.dump(new_dict,tpy)

import numpy as np
import json


def reform(type):
    if type=="Listing":
        return "enlisting"
    elif type=="Normal Text":
        return "normal_text"
    elif type=="Title":
         return "title"
    elif type in ["Image","Logo"]:
        return "picture"
    elif type=="Background":
        return "background"
    elif type in ["Footer","Institute","Author","Acknowledgement","Date","Noise", "Reference"]:
        return "footer"
    elif type=="Caption":
        return "caption"
    elif type=="Slide number":
        return "slide_number"
    elif type=="Listing Image":
        return "enlisting_image"
    else:
        raise TypeError(type)


with open("D://Thesis//landslide//data//Annotations//results//annotated_data//full_annotation.json") as annot:
    annotated=json.load(annot)
with open("D://Thesis//landslide//data//Annotations//results//annotated_data//types_categorized.json") as tps:
    categorized=json.load(tps)
total_score=0
total_elements=0
cat_elements=['title','enlisting', 'normal_text',  'picture','background', 'caption',  'slide_number', "footer","enlisting_image"]
ano_elements=['Background', 'Slide number', 'Normal Text', 'Footer', 'Date', 'Acknowledgement', 'Noise', 'Caption', 'Reference', 'Listing', 'Logo', 'Title', 'Author', 'Listing Image', 'Image', 'Institute']
cat_labels=["Title","Listing","Normal text","Picture","Background","Caption","Slide number","Footer","Listing image"]
matrix=[[0 for x in range(0,len(cat_elements))] for z in range(0,len(cat_elements))]
y_test=[]
pred=[]
for slide in categorized:
    an_types= annotated[slide]["regions"]
    cat_types=categorized[slide]
    for ind in range(0,len(an_types)):
        cat_type,an_type=None,None
        if "Type" in an_types[ind]["region_attributes"]:
            an_type=an_types[ind]["region_attributes"]["Type"]
        if str(ind) in cat_types:
            cat_type=cat_types[str(ind)]
        if cat_type!=None and an_type!=None:

            matrix[cat_elements.index(reform(an_type))][cat_elements.index(cat_type)]+=1
            total_elements+=1
            total_score+=int(cat_type==reform(an_type))
print(total_score/total_elements)
new_matrix=[[v/sum(x) for v in x] for x in matrix]

fig, ax = plt.subplots(figsize=[12,9])

g=sns.heatmap(new_matrix,cmap="Blues",ax=ax,xticklabels=cat_labels,yticklabels=cat_labels,linewidths=.5)

plt.show()
figure = g.get_figure()
figure.savefig("D:/Thesis/landslide/images_paper/annotations.svg")
