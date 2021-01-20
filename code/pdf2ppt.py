import tkinter as tk
import shutil
from tkinter import filedialog
from thesis_sieben_bocklandt.code.prototyping.pdf2xml import pdf2xml
from thesis_sieben_bocklandt.code.prototyping.xml2image import xml2image
from thesis_sieben_bocklandt.code.prototyping.xml_preparse2tree import preparse_xml
from thesis_sieben_bocklandt.code.prototyping.tree2features import tree2features
from thesis_sieben_bocklandt.code.prototyping.tree2RA import tree2RA
from thesis_sieben_bocklandt.code.prototyping.RA2archetype import RA2archetype
from thesis_sieben_bocklandt.code.prototyping.archetype2image import archetype2image
from thesis_sieben_bocklandt.code.prototyping.archetypes2slides import archetypes2slides
from thesis_sieben_bocklandt.code.prototyping.ppt_pdf_similarity import ppt_pdf_similarity
from thesis_sieben_bocklandt.code.prototyping.work_with_scores import work_with_scores

def pdf2ppt(pdf_file,output_directory,testing, images, clear_images=False):
    """
    A function tat groups all the functionality. It makes an xml from the given pdf, preparses this xml,
    assigns features to the elements in the preparsed xml and ...
    :param pdf_file: The path to the pdf_file
    :param output_directory: The wanted output_directory of the images etc
    :param testing: If it is for testing purposes
    :return:
    """
    if pdf_file=="":
        root = tk.Tk()
        root.withdraw()
        pdf_file = filedialog.askopenfilename()

    if output_directory=="":
        root = tk.Tk()
        root.withdraw()
        output_directory = filedialog.askdirectory()

    #FLOW
    print("-->PDF2XML")
    xml_file=pdf2xml(pdf_file,output_directory)
    print("-->preparse_xml")
    xml_tree = preparse_xml(xml_file,output_directory)
    #print("-->xml2image")
    if images or clear_images:
        xml2image(pdf_file,xml_tree,output_directory, False)
    print("-->tree2features")
    feature_tree = tree2features(xml_tree, xml_file,output_directory, True)
    #print("-->xml2image")
    if images:
        xml2image("",feature_tree,output_directory, True)
    print("-->tree2RA")
    powerpoint, tree_with_indexes, one_background=tree2RA(feature_tree, xml_file)
    print("-->RA2archetype")
    archetypes,changes=RA2archetype(powerpoint)
    #print("-->archetype2image")
    if images:
        archetype2image(output_directory,archetypes,changes)
    print("-->archetypes2slides")
    used_info = archetypes2slides(archetypes,tree_with_indexes, output_directory)
    print("-->ppt_pdf_similarities")
    scores=ppt_pdf_similarity(used_info,xml_file.replace(".xml","_preparsed.xml"), one_background)
    print("-->work_with_data")
    work_with_scores(scores, archetypes, output_directory)



    if testing:
        print("Map wordt verwijderd")
        shutil.rmtree(output_directory)
