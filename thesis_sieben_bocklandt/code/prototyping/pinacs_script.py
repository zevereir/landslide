import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
conf_path = os.getcwd()
sys.path.append(conf_path)
from thesis_sieben_bocklandt.code.prototyping.tree2RA import tree2RA
from thesis_sieben_bocklandt.code.prototyping.RA2archetype import RA2archetype
from thesis_sieben_bocklandt.code.prototyping.archetypes2slides import archetypes2slides
from thesis_sieben_bocklandt.code.prototyping.work_with_scores import work_with_scores
from thesis_sieben_bocklandt.code.prototyping.ppt_pdf_similarity import ppt_pdf_similarity
import argparse
#python thesis_sieben_bocklandt/code/prototyping/pinacs_script.py --data thesis_sieben_bocklandt/Data/test/RA_data --archetypes learned --force --equal-size --exp-name learned --cutoff 2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",default=None)
    parser.add_argument("--exp-name",default="baseline")
    parser.add_argument("--archetypes",default="baseline")
    parser.add_argument("--master",default="thesis_sieben_bocklandt/code/prototyping/MasterTemplate.pptx")
    parser.add_argument("--force",action="store_true")
    parser.add_argument("--cutoff",default=2)
    parser.add_argument("--equal-size",action="store_true")
    parser.add_argument("--beam-size",default=None)
    args = parser.parse_args()

    beam=args.beam_size
    name_output=args.archetypes+"_"+args.exp_name+"_"+str(args.cutoff)+"_"+str(beam)
    if beam!=None:
        beam=int(beam)

    source = Path(args.data).resolve()
    force_override=args.force
    data=source.stem.replace("_data","")
    feature_tree = ET.parse(source / (data + "_categorized.xml"))
    xml_file = source / (data + ".xml")
    ppt_path=Path(args.master)
    output = source
    if not (output / name_output).is_file() or force_override:
        powerpoint, tree_with_indexes, one_background = tree2RA(feature_tree, xml_file)
        archetypes, best_simil, times= RA2archetype(powerpoint, args.archetypes, int(args.cutoff), args.equal_size, beam)
        used_info = archetypes2slides(archetypes, tree_with_indexes, output,ppt_path,
                                      [(page.RA, page.n) for page in powerpoint.pages],False)
        scores = ppt_pdf_similarity(used_info, source / (data + "_preparsed.xml"), one_background)
        work_with_scores(scores, archetypes,times, source/"results",name_output, False,force_override)


if __name__ == "__main__":
    main()