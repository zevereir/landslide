import xml.etree.ElementTree as ET
from tree2features import calc_surface, amount_of_overlap



def ppt_pdf_similarity(ppt_info, xml_file, one_background):
    """"
    De functie die voor een bepaalde presentatie bekijkt hoeveel info er is meegekomen vanuit de pdf.
    Dit wordt gedaan door de elementen uit de gepreparsde xml-tree te vergelijken met de gebruikte info
    uit de slideshow. De score is het percentage van oppervlakte van de gebruikte elementen tov alle elementen"""
    xml_tree=ET.parse(xml_file)
    scores=[]
    responsive_scores=[]
    for page in xml_tree.getroot():
        info=ppt_info.pop(0)
        used_content=info[0]
        percentage=info[1]
        tables=[]
        page_size=[float(x) for x in page.attrib.get("bbox").split(",")]
        for i in used_content:
            if i.startswith("table_bbox_for_score_calc_"):
                table_bbox=[float(x) for x in i.strip()[27:-1].split(",")]
                tables.append(table_bbox)
        total_surface=0
        used_surface=0
        for element in page:
            bbox=[float(x) for x in element.attrib.get("bbox").split(",")]
            surface=calc_surface(bbox)
            total_surface+=surface
            if element.tag=="figure":
                src=element.attrib.get("src")
                if src.strip() in used_content:
                    used_surface+=surface
                elif (amount_of_overlap(bbox,page_size)[0]>0.8 and one_background):
                    total_surface-=surface
            elif element.tag=="textbox":
                used=True
                for text in element.text.split("\n"):
                    if len([True for x in used_content if text.strip() in x])==0:
                        if ord(text[0])<128:
                            used=False
                        else:
                            if len([text[1:].strip() in x for x in used_content])==0:
                                used=False
                if used:
                    used_surface+=surface

            elif element.tag=="rect":
                used=False
                for table in tables:
                    if amount_of_overlap(bbox,table)[0]==1:
                        used=True
                if used:
                    used_surface += surface
        score=min(round(used_surface/max(total_surface,1),4),1.0)
        scores.append(score)
        responsive_scores.append(percentage)
    return list(zip(scores,responsive_scores))

