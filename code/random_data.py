# import random
# import xml.etree.ElementTree as ET
# from pathlib import Path
# from tree2RA import tree2RA
# import os
# counter=0
# while counter!=1000:
#     print("COUNTER",counter)
#     sh=str(random.randint(1,840))
#     slideshow = "D://Thesis//landslide//data//american//"+sh+"_data//"+sh+"_categorized.xml"
#     tree= ET.parse(slideshow)
#     amount_of_slides=len(tree.getroot())
#     random_slide=random.randint(0,amount_of_slides-1)
#     already_done=os.listdir("D://Thesis//landslide//data//random_subset")
#     if sh+"_"+str(random_slide)+"_data" not in already_done:
#         slide=list(tree.getroot())[random_slide]
#         pages=ET.Element("pages")
#         pages.append(slide)
#         new_tree=ET.ElementTree(pages)
#         output=Path("D://thesis//landslide//data//random_subset//"+sh+"_"+str(random_slide)+"_data")
#         output.mkdir(exist_ok=True)
#         if not (output/"slide.xml").is_file():
#             Path.touch(output/"slide.xml")
#         new_tree.write(output/"slide.xml")
#         tree2RA(new_tree,output/"slide.xml")
#         counter+=1

import os

from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

#mapping the different xml-tags to the colored boxes



def xml2image(photo, tree, output):

    xml_tree=ET.parse(tree)
    print("XML parsen")
    root = xml_tree.getroot()
    rectangles_per_page=[]
    counter=0
    for page in root:
        attributes = page.attrib
        size = attributes.get("bbox").split(",")
        rectangles = [(float(size[2]), float(size[3]))]

        # print(size)
        for child in page:
            child.set("Annotation_index",str(counter))
            counter+=1
            child_attributes = child.attrib
            if len(child_attributes)!=0:
                child_size = child_attributes.get("bbox").split(",")
                x1 = float(child_size[0])
                y1 = float(child_size[1])
                x2 = float(child_size[2])
                y2 = float(child_size[3])
                length = abs(x2 - x1)
                width = abs(y2 - y1)
                if child.tag=="title":
                    color="y"
                    text=str(counter-1)+" (title)"
                elif child.tag=="image":
                    color="b"
                    text=str(counter-1)+" (image)"
                elif child.tag=="curve":
                    color="m"
                    text=str(counter-1)+" (curve)"
                else:
                    color="r"
                    text=str(counter-1)

                rectangles.append([x1, y2, length, width,text,color])
        xml_tree.write(tree)
        showImage_with_rectangles(output,photo,rectangles)
#
#
def showImage_with_rectangles(filename,path_to_image,rectangles):
    im = np.array(Image.open(path_to_image), dtype=np.uint8)
    shape=im.shape
    xml_shape=rectangles.pop(0)
    x=shape[1]
    y=shape[0]
    xml_x=xml_shape[0]
    xml_y=xml_shape[1]
    x_factor=x/xml_x
    y_factor=y/xml_y
    # Create figure and axes
    fig, ax = plt.subplots(1)
    # Display the image
    ax.imshow(im)
    for rectangle in rectangles:
        # Create a Rectangle patch (xy) upper left, width, height
        upper_left_x=rectangle[0]*x_factor
        upper_left_y=y-rectangle[1]*y_factor
        length=rectangle[2]*x_factor
        width=rectangle[3]*y_factor
        color=rectangle[5]
        rect = patches.Rectangle((upper_left_x,upper_left_y), length,width, linewidth=1,edgecolor=color, facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
        plt.text(upper_left_x,upper_left_y,rectangle[4],bbox=dict(facecolor=color, alpha=0.5))
    plt.axis("off")
    plt.savefig(filename)

    plt.close()
def map_tag(tag):
    if tag == "title":
        return "Title"
    elif tag == "normal_text":
        return "Normal Text"
    elif tag =="curve":
        return "Curve"
    elif tag=="table":
        return "Table"
    elif tag=="ref":
        return "Reference"
    elif tag=="curvetext":
        return "Text in curve"
    elif tag=="tabletext":
        return "Text in table"
    elif tag=="picture":
        return "Image"
    elif tag=="enlisting":
        return "Listing"
    elif tag=="enlisting_image":
        return "Listing Image"
    elif tag=="caption":
        return "Caption"
    elif tag=="background":
        return "Background"
    elif "rect":
        return "Rect"
    else:
        raise(ValueError(tag))



import os
from shutil import copyfile
from pathlib import Path
import xml.etree.ElementTree as ET
import json
all_slides = [x for x in os.listdir("D://Thesis//landslide//data//random_subset") if "annotated" not in x and "images" not in x and "annotations" not in x]
new_dict={}
for sh in all_slides:

#     print(sh)
#
    image="D://Thesis//landslide//data//random_subset//"+sh+"//"+sh.replace("_data","")+".jpg"

    img_size=os.path.getsize(image)
    tree="D://Thesis//landslide//data//random_subset//"+sh+"//slide.xml"
    parsed= ET.parse(tree)
    rectangles=[]
    tags=[]
    for page in parsed.getroot():
        bbox=[float(x) for x in page.attrib.get("bbox").split(",")]
        slide_size=(int(bbox[2]),int(bbox[3]))
        for child in page:
            rectangles.append([float(x) for x in child.attrib.get("bbox").split(",")])
            tags.append(map_tag(child.tag))
    regions=[]

    for id in range(0,len(rectangles)):
        rect=rectangles[id]
        shape_attributes={"name":"rect"}
        shape_attributes["x"]=rect[0]
        shape_attributes["y"]=slide_size[1]-rect[3]
        shape_attributes["width"]=rect[2]-rect[0]
        shape_attributes["height"]=rect[3]-rect[1]
        region_attributes={"Type":tags[id]}
        regions.append({"shape_attributes":shape_attributes,"region_attributes":region_attributes})
    new_dict[sh.replace("_data","")+".jpg"+str(img_size)]={"filename":sh.replace("_data","")+".jpg","filesize":img_size,"regions":regions,"file_attributes":{}}
with open("D://Thesis//landslide//data//random_subset//annotated_data.json", 'w') as fp:
    json.dump(new_dict, fp)




