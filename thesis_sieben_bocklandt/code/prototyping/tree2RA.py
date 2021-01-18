from thesis_sieben_bocklandt.code.prototyping.classes import *
RELATIONS={"b", "f", "m", "o", "s", "d", "eq", "di", "si", "oi", "mi", "fi", "bi"}

NOT_OVERLAPPING={"b","bi","m","mi"}
OVERLAPPING=RELATIONS-NOT_OVERLAPPING


def tree2RA(tree,xml_file):
    """ de functie die de geannoteerde xml_boom omzet naar een RA(rectangle algebra) voorstelling."""
    content_tags=["enlisting","normal_text","picture","table", "combined_pictures"]
    pages=[]
    page_index=0
    amount_of_slides = len(tree.getroot()[:])
    background_counter = 0
    one_background = False
    for page in tree.getroot():
        elements = page[:]
        background_indexes = [element for element in elements if element.tag=="background"]
        if len(background_indexes) > 0:
            background_counter += 1
    if background_counter / amount_of_slides > 0.8:
        one_background = True
    for page in tree.getroot():
        page_id=int(page.attrib.get("id"))
        index=0
        usefull_elements=[]
        page_size=[float(x) for x in page.attrib.get("bbox").split(",")]
        title_indices=[]
        background_indices=[]
        for element in page:
            bbox = [float(x) for x in element.attrib.get("bbox").split(",")]
            tag = element.tag
            new_element=None
            if  tag=="title":
                new_element=Title(index,bbox)
                title_indices.append(index)
            elif tag in content_tags:
                new_element=Content(index,bbox)
            elif tag=="background" and not one_background:
                new_element=Background(index,bbox)
                background_indices.append(index)
            if new_element is not None:
                usefull_elements.append(new_element)
                element.set("archetypal_index",str(index))
                index += 1
        rectangle_algebra=calc_RA_set(usefull_elements,page_size, title_indices,background_indices, page_id)
        pages.append(Page(usefull_elements,rectangle_algebra,page_index, len(usefull_elements)))
        page_index+=1
    tree.write(xml_file)
    return Powerpoint(pages), tree, one_background

def calc_RA_set(elements,page_size, title_indices, background_indices, page_id):
    """gebruik makend van alle nuttige elementen in een pagina maakt deze functie een RA-set op"""
    RA_set=set()
    for index1 in range(0,len(elements)):
        for index2 in range(index1+1,len(elements)):
            element1=elements[index1].bbox
            element2 = elements[index2].bbox
            relation=find_RA_relation(element1,element2)
            if "i" in relation[0]:
                RA_set.add(relation[0][0] + "-x+" + str(index2) + "_" + str(index1))
            else:
                RA_set.add(relation[0] + "-x+" + str(index1) + "_" + str(index2))
            if "i" in relation[1]:
                RA_set.add(relation[1][0] + "-y+" + str(index2) + "_" + str(index1))
            else:
                RA_set.add(relation[1] + "-y+" + str(index1) + "_" + str(index2))
            #inverse_relation=inverse(relation)
            #RA_set.add(inverse_relation[0] + "-x+" + str(index2) + "_" + str(index1))
            #RA_set.add(inverse_relation[1] + "-y+" + str(index2) + "_" + str(index1))
            # if relation[0] in OVERLAPPING:
            #     RA_set.add("overlapping"+ "-x+" + str(index1) + "_" + str(index2))
            #     RA_set.add("overlapping" + "-x+" + str(index2) + "_" + str(index1))
            # else:
            #     RA_set.add("not_overlapping" + "-x+" + str(index1) + "_" + str(index2))
            #     RA_set.add("not_overlapping" + "-x+" + str(index2) + "_" + str(index1))
            # if relation[1] in OVERLAPPING:
            #     RA_set.add("overlapping"+ "-y+" + str(index1) + "_" + str(index2))
            #     RA_set.add("overlapping" + "-y+" + str(index2) + "_" + str(index1))
            # else:
            #     RA_set.add("not_overlapping" + "-y+" + str(index1) + "_" + str(index2))
            #     RA_set.add("not_overlapping" + "-y+" + str(index2) + "_" + str(index1))

        # if index1 in title_indices:
        #     RA_set.add(find_position(elements[index1].bbox,page_size)+"+"+str(index1))
    if title_indices!=[]:
        for title in title_indices:
            RA_set.add("title+"+str(title))
    else:
        RA_set.add("no_title")
    if len(elements)-len(title_indices)==0:
        RA_set.add("no_content")
    for back in background_indices:
        RA_set.add("background+"+str(back))
    if page_id==1:
        RA_set.add("first_slide")
    return RA_set

def find_position(bbox,page_size):
    """bepaalde de relatieve positie van een object tov de gehele slide"""
    positie=""
    x_center=(bbox[0]+bbox[2])/2
    y_center = (bbox[1] + bbox[3]) / 2
    if x_center < 0.3*page_size[2]:
        positie+="links"
    elif x_center > 0.7*page_size[2]:
        positie+="rechts"
    else:
        positie+="middel"
    if y_center < 0.3*page_size[3]:
        positie+="onder"
    elif y_center > 0.7*page_size[3]:
        positie+="boven"
    else:
        positie+="middel"
    return positie


def inverse(relation):
    """bepaald de inverse van een relatie"""
    relations=["b","f","m","o","s","d","eq","di","si","oi","mi","fi","bi"]
    return (relations[len(relations)-relations.index(relation[0])-1],relations[len(relations)-relations.index(relation[1])-1])


def find_RA_relation(element1,element2):
    """bouwt de RA matrix op"""
    x_relation=allen_relation(element1[0],element1[2],element2[0],element2[2])
    y_relation = allen_relation(element1[1], element1[3], element2[1], element2[3])
    return (x_relation,y_relation)


def allen_relation(x11,x12,x21,x22):
    """wijst de correcte Allen relatie toe aan 2 elementen"""
    if x12 < x21:
        return "b"
    elif x22 < x11:
        return "bi"
    elif x11==x21:
        if x12==x22:
            return "eq"
        elif x12<x22:
            return "s"
        else:
            return "si"
    elif x12==x22:
        if x11>x21:
            return "f"
        else:
            return "fi"
    elif x12==x21:
        return "m"
    elif x22==x11:
        return "mi"
    elif x11 > x21 and x12<x22:
        return "d"
    elif x11 < x21 and x12>x22:
        return "di"
    elif x11<x21 and x12 < x22:
        return "o"
    else:
        return "oi"




