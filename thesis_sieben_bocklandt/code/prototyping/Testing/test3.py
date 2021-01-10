from thesis_sieben_bocklandt.code.prototyping.tree2RA import tree2RA
from thesis_sieben_bocklandt.code.prototyping.RA2archetype import RA2archetype
from thesis_sieben_bocklandt.code.prototyping.tree2features import tree2features
from thesis_sieben_bocklandt.code.prototyping.archetypes2slides import archetypes2slides
from thesis_sieben_bocklandt.code.prototyping.ppt_pdf_similarity import ppt_pdf_similarity
from thesis_sieben_bocklandt.code.prototyping.work_with_scores import work_with_scores
import xml.etree.ElementTree as ET
for i in range(1,73):
    print("------ "+str(i))
    test="data"+str(i)
    output="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\dataset\\"+test+"_data"
    path = output + "\\" + test + "_preparsed.xml"
    xml = output + "\\" + test + ".xml"
    tree = ET.parse(path)
    new_tree = tree2features(tree, xml, output, True)
    presentation,ra_tree, one_background = tree2RA(new_tree,output+"\\"+test+".xml")
    archetypes,changes=RA2archetype(presentation)
    used_info = archetypes2slides(archetypes,ra_tree,output)
    scores=ppt_pdf_similarity(used_info,output+"\\"+test+"_preparsed.xml", one_background)
    work_with_scores(scores, archetypes, output)