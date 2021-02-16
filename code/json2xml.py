import json
from PIL import Image
import xml.etree.ElementTree as ET
from xml.dom import minidom


def map_type(type):
    if type=="Listing":
        return "enlisting"
    elif type=="Normal Text":
        return "normal_text"
    elif type=="Title":
        return "title"
    elif type=="Image":
        return "picture"
    elif type=="Background":
        return "background"
    else:
        raise TypeError("type="+type)


with open("./data/Annotations/results/experiments.json") as fp:
    annotations=json.load(fp)
tree=ET.Element("pages")
for slide in list(annotations.keys()):

    print(slide)
    if "kopie" not in slide:
        image=Image.open("D://Thesis//landslide//data//Annotations//images//"+slide[0:slide.find(".png")+4])
        page_size=image.size
        page=ET.Element("page")
        page.set("bbox",str([0,0,page_size[0],page_size[1]])[1:-1])
        page.set("id",slide[1+slide.rfind("_"):slide.find(".png")])
        tree.append(page)
        regions=annotations[slide]["regions"]
        joins={}
        join_bbox={}
        for element in regions:
            region_attributes=element["region_attributes"]
            if "Join" in region_attributes:
                join=region_attributes["Join"]
                if "Type" in region_attributes:
                    type=region_attributes["Type"]
                else:
                    type=None
                if "Role" in region_attributes:
                    role=region_attributes["Role"]
                else:
                    role=None
                if ((join not in joins and type =="Normal text") or type=="Listing" or type=="Image") and role!=None:
                    joins[join]=(type,role)
                shape=element["shape_attributes"]
                x=float(shape["x"])
                y=page_size[1]-float(shape["y"])
                x2=x+float(shape["width"])
                y2=y+float(shape["height"])
                bbox=[x,y,x2,y2]
                if join not in join_bbox:
                   join_bbox[join]=bbox
                else:
                    jbbox=join_bbox[join]
                    join_bbox[join]=[min(jbbox[0],bbox[0]),min(jbbox[1],bbox[1]),max(jbbox[2],bbox[2]),max(jbbox[3],bbox[3])]
        print(joins)
        elements=[]
        joins_done=[]
        for element_id in range(0,len(regions)):
            element=regions[element_id]
            attributes=element["region_attributes"]
            type,Role,join=None,None,None
            shape=element["shape_attributes"]
            x=float(shape["x"])
            y=page_size[1]-float(shape["y"])
            x2=x+float(shape["width"])
            y2=y+float(shape["height"])
            bbox=[x,y,x2,y2]

            if "Type" in attributes:
                type=attributes["Type"]
            if "Role" in attributes:
                role=attributes["Role"]
            if "Join" in attributes:
                join=attributes["Join"]
                if join in joins:
                    bbox=join_bbox[join]
                    type=joins[join][0]
                    role=joins[join][1]
            if (join==None or join not in joins_done) and type!="Noise" and role!="Noise":
                if join!=None:
                    joins_done.append(join)
                elements.append((element_id,type,role,bbox))
        print(elements)
        for el in elements:
            if el[1] not in ["Footer", None, "Institute","Author","Acknowledgement","Listing Image","Date","Slide number","Reference", "Logo","Caption"]:
                child=ET.Element(map_type(el[1]))
                child.set("Role",el[2])
                child.set("bbox",str(el[3])[1:-1])
                child.set("id",str(el[0]))
                page.append(child)

xmlstr = minidom.parseString(ET.tostring(tree)).toprettyxml(indent="   ")
with open("./data/Annotations/results/annotated_data/annotated_categorized.xml", "w") as f:
    f.write(xmlstr)




