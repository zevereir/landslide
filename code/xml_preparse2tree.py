import xml.etree.ElementTree as ET
from thesis_sieben_bocklandt.code.prototyping.BMP import check_if_all_same_color
from thesis_sieben_bocklandt.code.prototyping.tree2features import amount_of_overlap
import os
from PIL import Image


def preparse_xml(xml_file, output_directory):
    """
    preparse the given xml_file by removing unneeded elements
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for page in root:
        attributes = page.attrib
        size = attributes.get("bbox").split(",")
        page_box = [float(x) for x in size]
        to_remove = set()
        rect_counter=0
        for child in page:
            if child.tag =="figure":  #removing the all_black .bmp files and empty figures
                child_box = [float(x) for x in child.attrib.get("bbox").split(",")]
                height_too_small = (abs(child_box[1] - child_box[3]) < 0.02 * abs(page_box[3] - page_box[1]))
                width_too_small = (abs(child_box[2] - child_box[0]) < 0.02 * abs(page_box[2] - page_box[0]))
                if height_too_small or width_too_small:
                    to_remove.add(child)
                elif len(child)!=1:
                    to_remove.add(child)
                elif child[0].tag=="figure":
                    child_attributes=child[0][0].attrib
                    child.set("src", child_attributes.get("src"))
                    child.set("width", child_attributes.get("width"))
                    child.set("height", child_attributes.get("height"))
                    child.remove(child[0])
                    if len(child)!=1:
                        to_remove.add(child)
                elif child[0].tag == "curve":
                    page.append(child[0])
                    to_remove.add(child)
                else:
                    child_attributes = child[0].attrib
                    source = child_attributes.get("src")
                    removed = False
                    if source==None:
                        to_remove.add(child)
                        removed=True
                    elif (source is not None) and source.endswith(".bmp"):
                        src = output_directory + "\\images\\" + source
                        all_same_color=check_if_all_same_color(src)
                        if all_same_color :
                            to_remove.add(child)
                            removed=True
                    elif (source is not None) and source.endswith("img"):
                        src = output_directory + "\\images\\" + source
                        img2png(src)
                        child_attributes["src"]=source.replace(".img",".png")
                        os.remove(src)
                    if not removed:
                        child.set("src", child_attributes.get("src"))
                        child.set("width", child_attributes.get("width"))
                        child.set("height", child_attributes.get("height"))
                        child.remove(child[0])
            if child.tag == "rect":  #removing the rect that is the background
                child_box = [float(x) for x in child.attrib.get("bbox").split(",")]
                overlap=amount_of_overlap(child_box,page_box)
                if overlap[1]>0.9:
                    to_remove.add(child)
                else:
                    rect_counter+=1
            if child.tag == "layout": #removing the layout part
                to_remove.add(child)
            if child.tag == "textbox": #combining the info from the text into the text-lines. If the line is all the same size etc, the text wil be deleted
                child_text=""
                child_font_size=0
                font_counter_line=0
                for line in child:
                    font_size_float=0
                    line_text=""
                    letters_remove=set()
                    font=""
                    ncolour=""
                    colourspace=""
                    font_size=""
                    added=False
                    all_the_same=True
                    empty=set()
                    font_counter=0
                    for letter in line:
                        letter_attributes = letter.attrib
                        if len(letter_attributes)==0:
                            line_text+=" "
                            empty.add(letter)
                        else:
                            if not added:
                                font=letter_attributes.get("font")
                                ncolour=letter_attributes.get("ncolour")
                                colourspace=letter_attributes.get("colourspace")
                                font_size=letter_attributes.get("size")
                                if font_size!=None:
                                    font_size_float+=float(font_size)
                                    font_counter+=1
                                added=True
                            if (font!=letter_attributes.get("font") or  ncolour != letter_attributes.get("ncolour")
                                    or colourspace != letter_attributes.get("colourspace") or font_size != letter_attributes.get("size")):
                                all_the_same=False
                            line_text += letter.text
                            letters_remove.add(letter)
                    for letter in empty:
                        line.remove(letter)
                    line.text = line_text
                    child_text += line_text+"\n"
                    child_font_size+=float(font_size_float)/font_counter
                    font_counter_line+=1
                    if all_the_same:
                        for letter in letters_remove:
                            line.remove(letter)
                        line.set("font",font)
                        line.set("ncolour",ncolour)
                        line.set("size",font_size)
                        line.set("colourspace",colourspace)
                child.set("size",str(child_font_size/font_counter_line))
                child_text=child_text[:-1]
                if child_text!=None:
                    child.text=child_text
        if rect_counter<6:
            for rect in page.findall("rect"):
                to_remove.add(rect)

        for child in to_remove:
            page.remove(child)
            if child.tag=="figure":
                for src in child:
                    source=src.attrib.get("src")
                    if source!=None:
                        os.remove(output_directory + "\\images\\" + source)
        for pic in page.findall("figure"):
            if pic.attrib.get("src")!= None and check_if_all_same_color(output_directory+"\\images\\"+pic.attrib.get("src")):
                page.remove(pic)
    tree.write(xml_file.replace(".xml","_preparsed.xml"))
    return tree


def img2png(src):
    """functie die .img files omzet naar png door de bytestream te lezen"""
    rawData = open(src, 'rb').read()
    # File size in bytes
    fs = len(rawData)
    name=src.split("\\")[-1].split(".")
    if len(name)!=5:
        dim=name[2].split("x")
    else:
        dim=name[3].split("x")

    height = int(dim[1])
    width = int(dim[0])
    try:
        image = Image.frombytes('RGB', (width, height), rawData, 'raw')
    except:
        image=Image.frombytes("1", (width, height), rawData, 'raw')
    image.save(src.replace(".img", ".png"))
