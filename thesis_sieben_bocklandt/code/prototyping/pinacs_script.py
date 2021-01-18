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
    parser.add_argument("--archetypes",default="baseline")
    parser.add_argument("--master",default="thesis_sieben_bocklandt/code/prototyping/MasterTemplate.pptx")
    parser.add_argument("--force",action="store_true")
    parser.add_argument("--cutoff",default=2)
    parser.add_argument("--equal-size",action="store_true")
    parser.add_argument("--beam-size",default=None)
    parser.add_argument("--set",default="all")
    parser.add_argument("--large-search", action="store_true")
    args = parser.parse_args()

    beam=args.beam_size
    if beam==None:
        beam_name="0"
    else:
        beam_name=str(beam)

    if beam!=None:
        beam=int(beam)
    if args.set=="all":
        categorized="_categorized.xml"
        preparsed="_preparsed.xml"
        set_name="all"
    elif args.set=="lessthanfive":
        categorized="_categorized_lessthanfive.xml"
        preparsed = "_preparsed_lessthanfive.xml"
        set_name="lessthanfive"
    elif args.set=="morethanfive":
        categorized = "_categorized_morethanfive.xml"
        preparsed = "_preparsed_morethanfive.xml"
        set_name="morethanfive"
    name_output = set_name + "_" + args.archetypes + "_" + str(args.cutoff) + "_" + beam_name + "_" + str(
        args.equal_size) + str(args.large_search)
    source = Path(args.data).resolve()
    force_override=args.force
    data=source.stem.replace("_data","")
    feature_tree = ET.parse(source / (data + categorized))

    ppt_path=Path(args.master)
    output = source
    if not (output / name_output).is_file() or force_override:
        powerpoint, tree_with_indexes, one_background = tree2RA(feature_tree, data+categorized)
        archetypes, best_simil, times= RA2archetype(powerpoint, args.archetypes, int(args.cutoff), args.equal_size, beam, args.large_search)
        used_info = archetypes2slides(archetypes, tree_with_indexes, output,ppt_path,
                                      [(page.RA, page.n) for page in powerpoint.pages],False)
        scores = ppt_pdf_similarity(used_info, source / (data + preparsed), one_background)
        work_with_scores(scores, archetypes,times, source/"results",name_output, False,force_override)


if __name__ == "__main__":
    main()