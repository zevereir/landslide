from PIL import Image
import operator
import xml.etree.ElementTree as ET
import numpy as np
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from EM import tenfold_EM
from operator import itemgetter
from math import ceil
POSSIBLE_ENLISTINGS={"-","*","+","%","$","?","~","_"}

def tree2features(tree, xml_file,output_directory, EM=False):
    """
    A function that assigns features like title, caption,... to the elements of a given xml_tree and returns this updated tree.
    :param xml_file: path to the original xml_file
    """
    GMMS=None
    if EM:
        GMMS=tenfold_EM(tree)

    images_path=output_directory+"\\images\\"
    mean_title=[]
    first_title_size=0
    for page in tree.getroot():
        attributes = page.attrib
        page_size = [float(x) for x in attributes.get("bbox").split(",")]
        tables = [table for table in categorize_rects(page,page_size) if len(table)>1]
        flattened_tables = [cell for table in tables for cell in table]
        curves = categorize_curves(page)
        categorized_images, images_bbox, enlistings=categorize_images(page,page_size,images_path)
        categorized_textboxes, title_box, title_size, add_to_mean, captions=categorize_textboxes(page,page_size,categorized_images, images_bbox, [[fig.get("src") for fig in l] for l in enlistings], mean_title, tables, curves, first_title_size, GMMS)
        if title_box!=[] and add_to_mean  :
            mean_title.append(title_box)
        if page.attrib.get("id")=="1":
            first_title_size=title_size



        #update the tree with the new features (remove lines and table-rects)
        to_remove=set()

        unique_element_id=0
        for element in page:
            element.set("unique_id",str(unique_element_id))
            if element.tag=="textbox":
                element.tag=categorized_textboxes[element.attrib.get("id")]
            elif element.tag=="figure":
                element.tag=categorized_images[element.attrib.get("src")]
            elif element.tag=="line":
                to_remove.add(element)
            elif element.tag=="rect":
                if [float(x) for x in element.attrib.get("bbox").split(",")] in flattened_tables:
                    to_remove.add(element)
            unique_element_id+=1
        for element in to_remove:
            page.remove(element)



        #make tables
        table_texts=page.findall("tabletext")
        removed=set()
        for table in tables:
                child=ET.Element("table")
                x1,y1,x2,y2=page_size[2],page_size[3],page_size[0],page_size[1]
                for cell in table:
                    x1=min(x1,cell[0])
                    y1=min(y1,cell[1])
                    x2=max(x2,cell[2])
                    y2=max(y2,cell[3])
                child.set("bbox",str(x1)+","+str(y1)+","+str(x2)+","+str(y2))
                for cell in table:
                    cell_element=ET.Element("cell")
                    for tabletext in table_texts:
                        if amount_of_overlap([float(x) for x in tabletext.attrib.get("bbox").split(",")],cell)[0]>0.8 and tabletext not in removed:
                            cell_element.append(tabletext)
                            page.remove(tabletext)
                            removed.add(tabletext)
                    cell_element.set("bbox",str(cell[0])+","+str(cell[1])+","+str(cell[2])+","+str(cell[3]))

                    child.append(cell_element)
                page.append(child)
        to_remove=set()
        for table in page.findall("table"):
            empty=True
            for cell in table:
                if len(cell)>0:
                    empty=False
            if empty:
                to_remove.add(table)
            else:
                amount_of_cells=len(table)
                table_bbox=[float(x) for x in table.attrib.get("bbox").split(",")]
                width=1
                total_width=0
                for cell in table:
                    cell_bbox=[float(x) for x in cell.attrib.get("bbox").split(",")]
                    if cell_bbox[2]==table_bbox[2] and total_width==0:
                        total_width=width
                    width+=1
                height=ceil(amount_of_cells/total_width)
                table.set("dimensions",str(total_width)+"/"+str(height))

        for table in to_remove:
            page.remove(table)

        #seperate textboxes to enlisting
        normal_texts=page.findall("normal_text")
        new_enlistings=[]
        for normal_text in normal_texts:
            first_character=normal_text.text[0]
            if first_character.isnumeric() or ord(first_character)>128 or first_character in POSSIBLE_ENLISTINGS:
                normal_bbox=[float(x) for x in normal_text.attrib.get("bbox").split(",")]
                if len(new_enlistings)==0:
                    new_enlistings.append([normal_text])
                else:
                    counter=0
                    added=False
                    for enlisting in new_enlistings:
                        is_this_enlisting=True
                        for item in enlisting:
                            item_bbox=[float(x) for x in item.attrib.get("bbox").split(",")]
                            if abs(item_bbox[0]-normal_bbox[0])>0.1*page_size[2]:
                                is_this_enlisting=False
                        if is_this_enlisting and not added:
                            new_enlistings[counter].append(normal_text)
                            added=True
                        counter+=1
                    if not added:
                        new_enlistings.append([normal_text])

        for new_enlisting in new_enlistings:
            if len(new_enlisting)>1:
                enlisting_element=ET.Element("enlisting")
                max_right=0
                min_left=page_size[2]
                min_down=page_size[3]
                max_up=0
                new_text=""
                unique_ids=[]
                for enl in new_enlisting:
                    new_text+=enl.text
                    bbox = [float(x) for x in enl.attrib.get("bbox").split(",")]
                    min_left=min(min_left,bbox[0])
                    min_down=min(min_down,bbox[1])
                    max_right=max(max_right,bbox[2])
                    max_up=max(max_up,bbox[3])
                    enlisting_element.append(enl)
                    unique_ids.append(enl.attrib.get("unique_id"))
                    page.remove(enl)
                enlisting_element.set("bbox", str(min_left) + "," + str(min_down) + "," + str(max_right) + "," + str(max_up))
                enlisting_element.set("unique_id",str(unique_ids))
                enlisting_element.text=new_text
                page.append(enlisting_element)

        #combining enlistings
        all_enlistings = page.findall("enlisting")
        new_enlistings = []
        for normal_enlisting in all_enlistings:
            normal_bbox = [float(x) for x in normal_enlisting.attrib.get("bbox").split(",")]
            if len(new_enlistings) == 0:
                new_enlistings.append([normal_enlisting])
            else:
                counter = 0
                added = False
                for enlisting in new_enlistings:
                    is_this_enlisting = True
                    for item in enlisting:
                        item_bbox = [float(x) for x in item.attrib.get("bbox").split(",")]
                        if abs(item_bbox[0] - normal_bbox[0]) > 0.1 * page_size[2] and 1.0 not in amount_of_overlap(item_bbox,normal_bbox):
                            is_this_enlisting = False
                    if is_this_enlisting and not added:
                        new_enlistings[counter].append(normal_enlisting)
                        added = True
                    counter+=1
                if not added:
                    new_enlistings.append([normal_enlisting])
        for new_enlisting in new_enlistings:
            if len(new_enlisting) > 1:
                enlisting_element = ET.Element("enlisting")
                max_right = 0
                min_left = page_size[2]
                min_down = page_size[3]
                max_up = 0
                new_text = ""
                unique_ids=[]
                for enl in new_enlisting:
                    new_text += enl.text
                    bbox = [float(x) for x in enl.attrib.get("bbox").split(",")]
                    min_left = min(min_left, bbox[0])
                    min_down = min(min_down, bbox[1])
                    max_right = max(max_right, bbox[2])
                    max_up = max(max_up, bbox[3])
                    enl.tag="normal_text"
                    unid=enl.attrib.get("unique_id")
                    if "[" in unid:
                        unique_ids+=list(unid[1:-1].replace("'","").split(","))
                    else:
                        unique_ids.append(unid)
                    enlisting_element.append(enl)
                    page.remove(enl)
                enlisting_element.set("bbox",str(min_left) + "," + str(min_down) + "," + str(max_right) + "," + str(max_up))
                enlisting_element.text=new_text
                enlisting_element.set("unique_id",str(unique_ids))
                page.append(enlisting_element)
        #combining normal_text and enlistings
        something_changed=True
        while something_changed:
            something_changed=False
            for enlisting in page.findall("enlisting"):
                enlisting_bbox=[float(x) for x in enlisting.attrib.get("bbox").split(",")]
                for normal_text in page.findall("normal_text")+page.findall("title"):
                    normal_bbox=[float(x) for x in normal_text.attrib.get("bbox").split(",")]
                    overlap1,overlap2=amount_of_overlap(enlisting_bbox,normal_bbox)
                    if 0.5 < overlap2 or abs(enlisting_bbox[1]-normal_bbox[3])<0.03*page_size[3]:
                        unid=enlisting.attrib.get("unique_id")
                        if "[" in unid:
                            unique_ids=list(unid[1:-1].replace("'","").split(","))
                        else:
                            unique_ids=[unid]
                        unique_ids.append(normal_text.attrib.get("unique_id"))
                        enlisting.append(normal_text)
                        page.remove(normal_text)
                        min_left = min(normal_bbox[0], enlisting_bbox[0])
                        min_down = min(normal_bbox[1], enlisting_bbox[1])
                        max_right = max(normal_bbox[2], enlisting_bbox[2])
                        max_up = max(normal_bbox[3], enlisting_bbox[3])
                        enlisting.set("bbox",str(min_left) + "," + str(min_down) + "," + str(max_right) + "," + str(max_up))
                        enlisting_bbox=[min_left,min_down,max_right,max_up]
                        enlisting.set("unique_id",str(unique_ids))
                        something_changed=True
        all_enlistings = page.findall("enlisting")
        new_enlistings = []
        for normal_enlisting in all_enlistings:
            normal_bbox = [float(x) for x in normal_enlisting.attrib.get("bbox").split(",")]
            if len(new_enlistings) == 0:
                new_enlistings.append([normal_enlisting])
            else:
                counter = 0
                added = False
                for enlisting in new_enlistings:
                    is_this_enlisting = True
                    for item in enlisting:
                        item_bbox = [float(x) for x in item.attrib.get("bbox").split(",")]
                        if abs(item_bbox[0] - normal_bbox[0]) > 0.1 * page_size[2] and 1.0 not in amount_of_overlap(
                                item_bbox, normal_bbox):
                            is_this_enlisting = False
                    if is_this_enlisting and not added:
                        new_enlistings[counter].append(normal_enlisting)
                        added = True
                    counter += 1
                if not added:
                    new_enlistings.append([normal_enlisting])
        for new_enlisting in new_enlistings:
            if len(new_enlisting) > 1:
                enlisting_element = ET.Element("enlisting")
                max_right = 0
                min_left = page_size[2]
                min_down = page_size[3]
                max_up = 0
                new_text = ""
                unique_ids=[]
                for enl in new_enlisting:
                    new_text += enl.text
                    bbox = [float(x) for x in enl.attrib.get("bbox").split(",")]
                    min_left = min(min_left, bbox[0])
                    min_down = min(min_down, bbox[1])
                    max_right = max(max_right, bbox[2])
                    max_up = max(max_up, bbox[3])
                    enl.tag = "normal_text"
                    unid=enl.attrib.get("unique_id")
                    if "[" in unid:
                        unique_ids+=list(unid[1:-1].replace("'","").split(","))
                    else:
                        unique_ids.append(unid)
                    enlisting_element.append(enl)
                    page.remove(enl)
                enlisting_element.set("bbox",
                                      str(min_left) + "," + str(min_down) + "," + str(max_right) + "," + str(max_up))
                enlisting_element.text = new_text
                enlisting_element.set("unique_id",unique_ids)
                page.append(enlisting_element)
        #removing enlisting images
        for item in page.findall("enlisting_image"):
            page.remove(item)

        #adding captions
        pictures=page.findall("picture")
        all_captions=page.findall("caption")
        pic_cap={}
        caps_id={}
        for combo in captions:
            pic=combo[1]
            cap_id=combo[0]
            cap_text=[(x.text,x.attrib.get("unique_id")) for x in all_captions if x.attrib.get("id")==cap_id][0]
            if pic in pic_cap.keys():
                pic_cap[pic]=pic_cap[pic]+"\n"+cap_text[0]
                caps_id[pic].append(cap_text[1])
            else:
                pic_cap[pic]=cap_text[0]
                caps_id[pic]=[cap_text[1]]
        for pic in pictures:
            pic_name=pic.attrib.get("src")
            if pic_name in pic_cap.keys():
                pic.set("caption",pic_cap[pic_name])
                pic.set("caption_id's",str(caps_id[pic_name]))
        for cap in all_captions:
            page.remove(cap)
        #combining pictures
        # changes=True
        # while changes:
        #     combined_pictures = []
        #     changes=False
        #     to_remove=set()
        #     pictures=page.findall("picture")+page.findall("combined_pictures")
        #     for picture in pictures:
        #         bbox = [float(x) for x in picture.attrib.get("bbox").split(",")]
        #         if combined_pictures==[]:
        #             combined_pictures.append([bbox,(picture,picture.attrib.get("src"))])
        #         else:
        #             assigned=False
        #             for combine in combined_pictures:
        #                 if (0 not in amount_of_overlap(combine[0],bbox) or touching(combine[0],bbox,page_size)) and not assigned:
        #                     combine.append((picture,picture.attrib.get("src")))
        #                     min_left=min(combine[0][0],bbox[0])
        #                     min_down = min(combine[0][1], bbox[1])
        #                     max_right = max(combine[0][2], bbox[2])
        #                     max_up = max(combine[0][3], bbox[3])
        #                     combine[0]=[min_left,min_down,max_right,max_up]
        #                     changes=True
        #                     assigned=True
        #
        #             if not assigned:
        #                 combined_pictures.append([bbox,(picture,picture.attrib.get("src"))])
        #     for combined in combined_pictures:
        #         if len(combined)>2:
        #             combined_element = ET.Element("combined_pictures")
        #             combined_element.set("bbox",",".join([str(x) for x in combined[0]]))
        #             names=[]
        #             cap=""
        #             for tup in combined[1:]:
        #                 el=tup[0]
        #                 caption=el.attrib.get("caption")
        #                 if caption !=None:
        #                     cap=cap+"\n"+caption
        #                 if el.tag=="picture":
        #                     combined_element.append(el)
        #                     names.append(tup[1])
        #                 else:
        #                     for child_pictures in el:
        #                         combined_element.append(child_pictures)
        #                     names+=[v.strip()[1:-1] for v in el.attrib.get("combined_sources")[1:-1].split(",")]
        #                 to_remove.add(el)
        #             combined_element.set("combined_sources",str(names))
        #             combined_element.set("caption",cap)
        #             page.append(combined_element)
        #     for i in to_remove:
        #         page.remove(i)

        mean_title_to_show=[]
        counter_title=0
        for title_index in range(0, len(mean_title)):
            title = mean_title[title_index]
            counter_title += (title_index + 1)
            if mean_title_to_show == []:
                mean_title_to_show += title
            else:
                for i in range(0, 4):
                    mean_title_to_show[i] += title[i] * (title_index + 1)
        if mean_title_to_show!=[]:
            for i in range(0,4):
                mean_title_to_show[i]/= counter_title
            page.set("mean_title",str(mean_title_to_show))

        name=0
        page_id=page.attrib.get("id")
        to_remove=set()
        for combined_image in page.findall("combined_pictures"):
            picture_name="combined_"+page_id+"_"+str(name)+".png"
            combine_pictures(combined_image,output_directory,picture_name)
            picture_element=ET.Element("picture")
            picture_element.set("src",picture_name)
            picture_element.set("bbox",combined_image.attrib.get("bbox"))
            picture_element.set("name","combined_"+str(name))
            picture_element.set("combined_sources",combined_image.attrib.get("combined_sources"))
            picture_element.set("caption",combined_image.attrib.get("caption"))
            to_remove.add(combined_image)
            page.append(picture_element)
            name+=1
        for i in to_remove:
            page.remove(i)
    tree.write(xml_file.replace(".xml", "_categorized.xml"))
    return tree

def combine_pictures(combined_picture,output_directory,name):
    """een functie die verschillende elkaar overlappende fotos combineerd tot 1 foto"""
    full_bbox=[float(x) for x in combined_picture.attrib.get("bbox").split(",")]
    width=full_bbox[2]-full_bbox[0]
    height=full_bbox[3]-full_bbox[1]
    dir = output_directory+"\\Images\\"
    sources=[]
    x_positions=[]
    y_positions=[]
    bbox_widths=[]
    bbox_heights=[]
    for img in combined_picture:
        sources.append(dir+img.attrib.get("src"))
        bbox=[float(x) for x in img.attrib.get("bbox").split(",")]
        x_positions.append(bbox[0]-full_bbox[0])
        y_positions.append(bbox[3]-full_bbox[1])
        bbox_widths.append(bbox[2]-bbox[0])
        bbox_heights.append(bbox[3]-bbox[1])

    images = [Image.open(x) for x in sources]
    total_width = 2000
    max_height = int(total_width*height/width)
    factor=total_width/width
    new_im = Image.new('RGBA', (total_width, max_height))
    for index in range(0,len(images)):
        im=images[index]
        new_x_size=int(factor * bbox_widths[index])
        new_y_size=int(factor * bbox_heights[index])
        if new_x_size>0 and new_y_size>0:
            im=im.resize((new_x_size,new_y_size),Image.NEAREST)
        new_im.paste(im, (int(factor*x_positions[index]),int(max_height-factor*y_positions[index])))
    new_im.save(dir+name)


def calc_slide_number_score(page_size, bbox, text):
    """
    calculates the probability that the given bbox-text combo is a slide number
    """
    score=0
    text=text.replace(" ","")
    factor=0.2
    if amount_of_overlap(bbox,[0,0,factor*page_size[2],factor*page_size[3]])[0]==1.0: #lower left
        score+=1
    elif amount_of_overlap(bbox,[(1-factor)*page_size[2],0,page_size[2],factor*page_size[3]])[0]==1.0: #lower right
        score+=1
    elif amount_of_overlap(bbox, [0,(1-factor) * page_size[3], factor * page_size[2],page_size[3]])[0] == 1.0: #upper left
        score+=1
    elif amount_of_overlap(bbox, [(1-factor) * page_size[2], (1-factor) * page_size[3],page_size[2],page_size[3]])[0] == 1.0: #upper right
        score+=1
    if text.isnumeric() or ("\\" in text and text[:text.find("\\")].isnumeric() and text[text.find("\\")+1:].isnumeric() ) or ("/" in text and text[:text.find("/")].isnumeric() and text[text.find("/")+1:].isnumeric() ):
        score+=2
    return score/3

def calc_title_score(page_size,bbox,id, max_font_size, page_id,mean_title, first_title_size, font_size, text,GMMS):
    """
      calculates the probability that the given bbox-id-font_size combo is a title
    """
    score = 0
    gmm_score = 0
    if GMMS != None:
        Y = np.array([[(bbox[0]+bbox[2])/(2*page_size[2])], [(bbox[1]+bbox[3])/(2*page_size[3])]])
        for GMM in GMMS:
            gmm_means = GMM.means_.tolist()
            max_mean = max(gmm_means, key=itemgetter(1))
            prediction = GMM.predict(Y.T)
            if max_mean == gmm_means[prediction[0]]:
                gmm_score += 1
    factor=0+(page_id!=1)*0.6
    size_score=1+(mean_title==[])*3
    if bbox[1]>factor*page_size[3]:
        score +=2
    if id == max_font_size:
        score += size_score
    counter=0
    mean=[]
    for title_index in range(0,len(mean_title)):
        title=mean_title[title_index]
        counter += (title_index+1)
        if mean==[]:
            mean+=title
        else:
            for i in range(0,4):
                mean[i] += title[i]*(title_index+1)
    add_to_mean=False
    if mean != []:
        for i in range(0,4):
            mean[i] /= counter
        overlap1,overlap2 = amount_of_overlap(bbox,mean)
        if overlap1 > 0.2 or overlap2>0.2 or gmm_score>7:
            score+=4
            add_to_mean=True
        elif font_size-first_title_size>-10:
            score+=4
    if mean_title==[] and bbox[1] > 0.6*page_size[3]:
        add_to_mean=True
    if ord(text[0])>128 or text[0] in POSSIBLE_ENLISTINGS:
        return 0,add_to_mean
    return score/7,add_to_mean

def calc_reference(inner_rectangle, bbox, text):
    """
      calculates the probability that the given bbox-text combo is a reference
    """
    lower_text=text.lower().replace(" ","")
    score=0
    if amount_of_overlap(bbox, inner_rectangle)[0]==0:
        score +=1
    if lower_text.startswith("[") and lower_text.endswith("]"):
        score +=2
    elif lower_text.startswith("source") or lower_text.startswith("src")or lower_text.startswith("ref"):
        score +=2
    else:
        validate = URLValidator()
        try:
            validate(text)
            score +=2
        except ValidationError:
            pass
    return score/3

def calc_enlisting(page_size,bbox, images_bbox, enlistings, text):
    """
      calculates the probability that the given bbox is an enlisting
    """
    score = 0
    nb_lines=len(text)
    counter_of_lines=0
    for line in text:
        if ord(line[0])>128 or line[0] in POSSIBLE_ENLISTINGS: #not in Ascii
            counter_of_lines+=1
    if nb_lines>5:
        score += 2*(counter_of_lines/nb_lines > 0.2)
    else:
        score += 2 * (counter_of_lines / nb_lines > 0.66)
    if score==0:
        stop_iterating=False
        for list in enlistings:
            if not stop_iterating:
                enlisting=True
                counter=0
                for item in list:
                    item_bbox=images_bbox[item]
                    if item_bbox[1] < bbox[1] or item_bbox[3]>bbox[3] or (1.0 not in amount_of_overlap(item_bbox,bbox) and abs(item_bbox[2]-bbox[0])>0.05*page_size[2]):
                        counter+=1
                if counter/len(list) >0.5:
                    enlisting=False
                if enlisting:
                    stop_iterating=True
                    score+=2
    if nb_lines>1:
        score +=1
    return score/3

def calc_caption(page_size,bbox, images_bbox, categorized_images, nb_lines):
    """
      calculates the probability that the given bbox is a caption

    """
    pic=None
    score=0
    for img in categorized_images:
        if categorized_images[img]=="picture" and score ==0:
            img_bbox=images_bbox[img]
            if (bbox[0]> img_bbox[0] or img_bbox[0]-bbox[0] < 0.05*page_size[2]) and (bbox[2]< img_bbox[2] or bbox[2]-img_bbox[2] < 0.05*page_size[2]) and 0<=img_bbox[1]-bbox[3] <= 0.2*page_size[3]:
                score +=3
                pic=img

    if nb_lines==1:
        score+=1
    return score/4, pic

def calc_tabletext(bbox,tables):
    """
      calculates the probability that the given bbox is tabletext
    """
    for table in tables:
        for cell in table:
            if amount_of_overlap(bbox,cell)[0]>0.8:
                return 1.0
    return 0

def calc_curvetext(bbox,curves):
    """  calculates the probability that the given bboxis curvetext """
    for curve in curves:
        if amount_of_overlap(bbox,curve)[0]>0.8:
            return 1.0
    return 0
def amount_of_overlap(bbox1,bbox2):
    """
    calculates the amount of overlap between two bboxes. The relative % for each of the bboxes is returned
    """
    if (bbox1[0]>bbox2[2] or bbox1[2] < bbox2[0] or bbox1[1] > bbox2[3] or bbox2[1] > bbox1[3]):
        return (0,0)
    surface1=(bbox1[2]-bbox1[0])*(bbox1[3]-bbox1[1])
    surface2 = (bbox2[2] - bbox2[0])*(bbox2[3] - bbox2[1])
    surface_overlap=abs(min(bbox1[2],bbox2[2])-max(bbox1[0],bbox2[0]))*abs(min(bbox1[3],bbox2[3])-max(bbox1[1],bbox2[1]))
    if surface1==0 or surface2==0:
        return (0,0)
    overlap1=surface_overlap/surface1
    overlap2=surface_overlap/surface2
    return (overlap1,overlap2)

def check_if_same_image(path1,path2):
    """
    checks if the images in the two paths are the same
    """
    try:
        im1 = Image.open(path1)
        im2 = Image.open(path2)
    except:
        return False

    return list(im1.getdata()) == list(im2.getdata())

def find_biggest_font_size(page):
    """
    Finds the textbox_id with the biggest font_size.
    :param page:
    :return:
    """
    max_font_size=0
    id=-1
    for child in page.iter("textbox"):
        if "size" in child.attrib.keys():
            text_box_size=float(child.attrib.get("size"))
            if text_box_size > max_font_size:
                max_font_size=text_box_size
                id=child.attrib.get("id")
        else:
            mean_font_size=0
            counter=0
            for line in child:
                if "size" in line.attrib.keys():
                    mean_font_size+=float(line.attrib.get("size"))
                    counter+=1
                else:
                    mean_line=0
                    counter_line=0
                    for word in line:
                        if len(word.attrib)!=0:
                            mean_line+=float(word.attrib.get("size"))
                            counter_line+=1
                    mean_font_size+=mean_line/counter_line
                    counter+=1
            mean_font_size/=counter
            if mean_font_size > max_font_size:
                max_font_size=mean_font_size
                id=child.attrib.get("id")
    return id,max_font_size

def categorize_rects(page, page_size):
    """
    categorize all rectangle elements
    """
    all_rects=page.findall("rect")
    tables=[]
    for rect in all_rects:
        bbox =[float(x) for x in rect.attrib.get("bbox").split(",")]
        if tables==[]:
            tables.append([bbox])
        else:
            counter=0
            added=False
            for table in tables:
                connects=False
                for cell in table:
                    if not connects:
                        if (bbox[1] == cell[1] and (abs(bbox[0]-cell[2])<0.05*page_size[2] or abs(bbox[2]-cell[0])<0.05*page_size[2])) or (bbox[0]==cell[0] and abs(bbox[3]-cell[1])<0.05*page_size[3] or abs(bbox[1]-cell[3])<0.05*page_size[3]):
                            connects=True
                if connects and bbox not in table:
                    added=True
                    table.append(bbox)
                    tables[counter]=table[:]
                counter+=1
            if not added:
                tables.append([bbox])
    return tables


def calc_surface(bbox):
    return (bbox[2]-bbox[0])*(bbox[3]-bbox[1])

def touching(bbox1,bbox2,page_size):
    if bbox1[1]<=bbox2[1]<=bbox1[3]<= bbox2[3]or bbox2[1]<=bbox1[1]<=bbox2[3]<= bbox1[3]:
        return abs(bbox1[0]-bbox2[2])<0.03*page_size[2] or abs(bbox2[0]-bbox1[2])<0.03*page_size[2]
    if bbox1[0]<=bbox2[0]<=bbox1[2]<= bbox2[2]or bbox2[0]<=bbox1[0]<=bbox2[2]<= bbox1[2]:
        return abs(bbox1[1]-bbox2[3])<0.03*page_size[3] or abs(bbox2[1]-bbox1[3])<0.03*page_size[3]
    return False




def categorize_curves(page):
    """
    categorize all curves in the page
    """
    curves=set()
    for curve in page.findall("curve"):
        curves.add(tuple([float(x) for x in curve.attrib.get("bbox").split(",")]))
    return curves

def categorize_images(page,page_size, images_path):
    """
    categorize all the images in the page
    """
    categorized_images={}
    images_bbox={}
    enlistings = []
    all_figures = page.findall("figure")
    for fig in page.iter("figure"):
        images_bbox[fig.attrib.get("src")]=[float(x) for x in fig.attrib.get("bbox").split(",")]
        is_enlisted = False
        for enlisting in enlistings:
            if fig in enlisting:
                is_enlisted = True

        if not is_enlisted:
            current_enlisting = [fig]
            all_figures.remove(fig)
            background=False
            fig_size = [float(x) for x in fig.attrib.get("bbox").split(",")]
            if amount_of_overlap(fig_size, page_size)[1] > 0.8:
                background=True

            else:
                fig_path = images_path + fig.attrib.get("src")
                to_remove=set()
                for other in all_figures:
                    other_path = images_path + other.attrib.get("src")
                    smallest_width = 0.1 * page_size[2]
                    height_diff=0.2*page_size[3]
                    other_bbox = [float(x) for x in other.attrib.get("bbox").split(",")]
                    if check_if_same_image(fig_path, other_path) and abs(fig_size[0] - other_bbox[0]) < smallest_width and abs(calc_surface(fig_size)-calc_surface(other_bbox))<0.01*calc_surface(page_size):
                        needs_to_be_added=False
                        if current_enlisting!=[]:
                            if abs([float(x) for x in current_enlisting[-1].attrib.get("bbox").split(",")][1]-other_bbox[3])<height_diff:
                                needs_to_be_added=True
                        else:
                            if abs(fig_size[1]-other_bbox[3])<height_diff:
                                needs_to_be_added=True
                        if needs_to_be_added:
                            current_enlisting.append(other)
                            to_remove.add(other)
                for other in to_remove:
                    all_figures.remove(other)
            if background:
                categorized_images[fig.attrib.get("src")] = "background"
            elif len(current_enlisting) != 1:
                for enl in current_enlisting:
                    categorized_images[enl.attrib.get("src")]="enlisting_image"
                enlistings.append(current_enlisting)
            else:
                categorized_images[fig.attrib.get("src")] = "picture"
    return categorized_images,images_bbox, enlistings

def categorize_textboxes(page,page_size,categorized_images, images_bbox, enlistings, mean_title, tables, curves, first_title_size,GMMS):
    """
    categorize all textboxes in the page using the separate probabilities for each textbox. The highest probability is assigned
    """
    categorized_textboxes={}
    biggest_font_size_textbox_id,title_size = find_biggest_font_size(page)
    inner_rectangle = [0.1*page_size[2],0.1*page_size[3],0.9*page_size[2],0.9*page_size[3]]
    page_id=int(page.attrib.get("id"))
    add_to_mean_result=False
    max_title_prob=0
    all_titles=[]
    captions=[]
    for textbox in page.iter("textbox"):
        scores={}
        box_size = [float(x) for x in textbox.attrib.get("bbox").split(",")]
        id = textbox.attrib.get("id")
        size=textbox.attrib.get("size")
        if size is None:
            size=0
        else:
            size=float(size)
        scores["slide_number"]=calc_slide_number_score(page_size, box_size, textbox[0].text)
        scores["title"],add_to_mean=calc_title_score(page_size,box_size, id,biggest_font_size_textbox_id, page_id,mean_title, first_title_size, size, textbox.text,GMMS)
        scores["ref"]=calc_reference(inner_rectangle,box_size,textbox[0].text)
        scores["enlisting"]=calc_enlisting(page_size,box_size,images_bbox,enlistings,[x.text for x in textbox[:]])
        scores["caption"], caption_pic = calc_caption(page_size,box_size, images_bbox, categorized_images, len(textbox[:]))
        scores["tabletext"]=calc_tabletext(box_size,tables)
        scores["curvetext"]=calc_curvetext(box_size,curves)
        #the baseline score is 0.5
        scores["normal_text"]=0.5
        categorized_textboxes[id]=max(scores.items(), key=operator.itemgetter(1))[0]
        if categorized_textboxes[id] == "title":
            max_title_prob=max(max_title_prob,scores["title"])
            title_box = box_size*(page_id>1)
            all_titles.append((id, scores, title_box))
            if add_to_mean:
                add_to_mean_result=True
        elif categorized_textboxes[id] =="caption":
            captions.append((id,caption_pic))

    final_title_box=[]
    box_chosen=False
    for title in all_titles:
        id=title[0]
        scores=title[1]
        if scores["title"] != max_title_prob or box_chosen:
            categorized_textboxes[id]="normal_text"
        elif not box_chosen:
            final_title_box=title[2]
            box_chosen=True

    return categorized_textboxes, final_title_box, title_size, add_to_mean_result, captions

