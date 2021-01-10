import sys
import os
import xml.etree.ElementTree as ET
conf_path = os.getcwd()
sys.path.append(conf_path)
from thesis_sieben_bocklandt.code.prototyping.tree2RA import tree2RA
from thesis_sieben_bocklandt.code.prototyping.RA2archetype import RA2archetype
from thesis_sieben_bocklandt.code.prototyping.archetypes2slides import archetypes2slides
from thesis_sieben_bocklandt.code.prototyping.work_with_scores import work_with_scores
from thesis_sieben_bocklandt.code.prototyping.ppt_pdf_similarity import ppt_pdf_similarity
import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",default=None)
    parser.add_argument("--exp-name",default="baseline")
    args = parser.parse_args()

    source = args.data.replace("/","\\") #bvb landslide_data//1_data
    name_output=args.exp_name
    if source.endswith("\\"):
        source=source[:-1]
    data=source[source.rfind("\\")+1:].replace("_data","")
    feature_tree = ET.parse(source+"\\" + data + "_categorized.xml")
    xml_file = source+"\\" + data + ".xml"
    output = source
    powerpoint, tree_with_indexes, one_background = tree2RA(feature_tree, xml_file)
    archetypes, changes = RA2archetype(powerpoint)
    used_info = archetypes2slides(archetypes, tree_with_indexes, output,
                                  [(page.RA, page.n) for page in powerpoint.pages],False)
    scores = ppt_pdf_similarity(used_info, xml_file.replace(".xml", "_preparsed.xml"), one_background)
    work_with_scores(scores, archetypes, source,"\\results\\"+name_output, False)


if __name__ == "__main__":
    main()