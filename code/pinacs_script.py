import os
from pathlib import Path
import xml.etree.ElementTree as ET
from tree2RA import tree2RA
from RA2archetype import RA2archetype
from archetypes2slides import archetypes2slides
from work_with_scores import work_with_scores
from ppt_pdf_similarity import ppt_pdf_similarity
import argparse
#python thesis_sieben_bocklandt/code/prototyping/pinacs_script.py --data thesis_sieben_bocklandt/Data/test/RA_data --archetypes learned --force --equal-size --exp-name learned --cutoff 2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",default=None)
    parser.add_argument("--archetypes",default="baseline")
    parser.add_argument("--force",action="store_true")
    parser.add_argument("--cutoff",default=0)
    parser.add_argument("--equal-size",action="store_true")
    parser.add_argument("--beam-size",default=None)
    parser.add_argument("--set",default="all")
    parser.add_argument("--run",default="1-1")
    parser.add_argument("--searcher",default="greedy")
    parser.add_argument("--single-content",action="store_true")
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
        if args.equal_size:
            raise(AttributeError("--equal-size is not allowed with --set morethanfive"))
        categorized = "_categorized_morethanfive.xml"
        preparsed = "_preparsed_morethanfive.xml"
        set_name="morethanfive"


    name_output = args.searcher+"_"+set_name + "_" + args.archetypes + "_" + str(args.cutoff) + "_" + beam_name + "_" + str(args.equal_size)+"_"+args.run
    if args.single_content:
        name_output="filtered_"+name_output
    source = Path(args.data).resolve()
    force_override=args.force
    data=source.stem.replace("_data","")
    feature_tree = ET.parse(source / (data + categorized))


    output = source
    if ".json" not in name_output:
        name_output+=".json"
    # print(output /"results"/ name_output)
    if not (output /"results"/ name_output).is_file() or force_override:
        powerpoint, tree_with_indexes, one_background = tree2RA(feature_tree, data+categorized)
        i, n = map(int, args.run.split("-"))
        size = len(powerpoint.pages) // n
        if i==n:
            powerpoint.pages = powerpoint.pages[(i-1) * size : ]
        else:
            powerpoint.pages = powerpoint.pages[(i-1) * size : min(i * size, len(powerpoint.pages))]

        results, results_json= RA2archetype(powerpoint, args.archetypes, int(args.cutoff), args.equal_size, beam, args.searcher, args.single_content)
        # used_info = archetypes2slides(archetypes, tree_with_indexes, output,ppt_path,
        #                               [(page.RA, page.n) for page in powerpoint.pages],False)
        # scores = ppt_pdf_similarity(used_info, source / (data + preparsed), one_background)
        work_with_scores(results, source/"results",name_output, False,force_override, results_json)

    else:
        print(output /"results"/ name_output)


if __name__ == "__main__":
    main()