
# import os
# from shutil import copyfile
# from pathlib import Path
# import xml.etree.ElementTree as ET
# import json
# all_slides = [x for x in os.listdir("D://Thesis//landslide//data//random_subset") if "annotated" not in x and "images" not in x and "annotations" not in x]
# new_dict={}
# for sh in all_slides:
#
# #     print(sh)
# #
#     image="D://Thesis//landslide//data//random_subset//"+sh+"//"+sh.replace("_data","")+".jpg"
#
#     img_size=os.path.getsize(image)
#     tree="D://Thesis//landslide//data//random_subset//"+sh+"//slide.xml"
#     parsed= ET.parse(tree)
#     rectangles=[]
#     tags=[]
#     for page in parsed.getroot():
#         bbox=[float(x) for x in page.attrib.get("bbox").split(",")]
#         slide_size=(int(bbox[2]),int(bbox[3]))
#         for child in page:
#             rectangles.append([float(x) for x in child.attrib.get("bbox").split(",")])
#             tags.append(map_tag(child.tag))
#     regions=[]
#
#     for id in range(0,len(rectangles)):
#         rect=rectangles[id]
#         shape_attributes={"name":"rect"}
#         shape_attributes["x"]=rect[0]
#         shape_attributes["y"]=slide_size[1]-rect[3]
#         shape_attributes["width"]=rect[2]-rect[0]
#         shape_attributes["height"]=rect[3]-rect[1]
#         region_attributes={"Type":tags[id]}
#         regions.append({"shape_attributes":shape_attributes,"region_attributes":region_attributes})
#     new_dict[sh.replace("_data","")+".jpg"+str(img_size)]={"filename":sh.replace("_data","")+".jpg","filesize":img_size,"regions":regions,"file_attributes":{}}
# with open("D://Thesis//landslide//data//random_subset//annotated_data.json", 'w') as fp:
#     json.dump(new_dict, fp)
#
#
#
import os
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image
all_images=os.listdir("D://Thesis//landslide//data//Annotations//images")
with open("D://Thesis//landslide//data//Annotations//annotated_data.json") as fp:
    annotations = json.load(fp)
for i in range(1,631):
    print("Slideshow",i)
    folder=Path("D://Thesis//landslide//data//Main//"+str(i)+"_data")
    tree = ET.parse(folder/(str(i)+"_preparsed.xml"))
    for element in tree.getroot():
        page_size=[int(float(x)) for x in element.attrib.get("bbox").split(",")][2:]
        page_id=element.attrib.get("id")

        im_name=[im for im in all_images if "_"+str(i)+"_"+str(int(page_id)-1)+".png" in im][0]

        im_path=Path("D://Thesis//landslide//data//Annotations//images")/im_name
        image = Image.open(im_path)
        image=image.resize(page_size)
        image.save(im_path)
        im_size = os.stat(im_path).st_size
        rectangles=[]
        for child in element:
            rectangles.append([float(x) for x in child.attrib.get("bbox").split(",")])
        regions=[]
        for id in range(0,len(rectangles)):
                rect=rectangles[id]
                shape_attributes={"name":"rect"}
                shape_attributes["x"]=rect[0]
                shape_attributes["y"]=page_size[1]-rect[3]
                shape_attributes["width"]=rect[2]-rect[0]
                shape_attributes["height"]=rect[3]-rect[1]
                region_attributes={}
                regions.append({"shape_attributes":shape_attributes,"region_attributes":region_attributes})
        annotations[im_name+str(im_size)]={"filename":im_name,"filesize":im_size,"regions":regions,"file_attributes":{}}
with open("D://Thesis//landslide//data//Annotations//annotated_data.json", 'w') as fp:
    json.dump(annotations, fp)