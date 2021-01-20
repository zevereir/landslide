import itertools
from functools import lru_cache
import json
from thesis_sieben_bocklandt.code.prototyping.classes import *
from thesis_sieben_bocklandt.code.prototyping.tree2RA import NOT_OVERLAPPING, OVERLAPPING
import thesis_sieben_bocklandt.code.prototyping.globals as glob
from thesis_sieben_bocklandt.code.prototyping.search import BreadthSearcher, GreedySearcher, count_objects, Predicate, similarity_optimal, apply
from datetime import datetime

def RA2archetype(powerpoint, arch_to_use, cutoff, equal_size, beam, searcher_name):
    """"
    De functie die een slideshow uitgedrukt in RA-algebra omzet naar archetypes.
    Deze archetypes zijn de basisvormen van de uiteindelijke powerpoint. Deze functie geeft archetype-objecten terug
    met daarin de juiste geanoteerde content_indexes die later samen met de categorized xml terug de slide kunnen opbouwen."""
    archs_to_use=[]
    master_archetypes = {}
    if arch_to_use=="baseline":
        with open('thesis_sieben_bocklandt/code/prototyping/archetypes/baseline.json') as json_file:
            arch_dict = json.load(json_file)
        for i in range(0, len(arch_dict)):
            baseline_archeypes=arch_dict[str(i)]
            for arch in baseline_archeypes:
                base_arch=frozenset(Predicate.from_string_sieben(s) for s in arch)
                archs_to_use.append(base_arch)
                if base_arch in master_archetypes.keys():
                    master_archetypes[base_arch].add((i,-1))
                else:
                    master_archetypes[base_arch]={(i,-1)}

    elif arch_to_use=="learned":
        with open('thesis_sieben_bocklandt/code/prototyping/archetypes/learned.json') as json_file:
            arch_dict = json.load(json_file)
        for i in range(0, len(arch_dict)):
            arch = arch_dict[str(i)]
            for key in range(0, len(arch)):
                master=arch[str(key)]
                for z in master:
                    base_arch = frozenset(Predicate.from_string_sieben(s) for s in z)
                    archs_to_use.append(base_arch)
                    if base_arch in master_archetypes.keys():
                        master_archetypes[base_arch].add((i, key))
                    else:
                        master_archetypes[base_arch] = {(i, key)}
    elif arch_to_use=="masters":
        with open('thesis_sieben_bocklandt/code/prototyping/archetypes/masters.json') as json_file:
            arch_dict = json.load(json_file)
        for i in range(0, len(arch_dict)):
            arch = arch_dict[str(i)]
            for key in range(0, len(arch)+1):
                if key!=25:
                    master=arch[str(key)]
                    for z in master:
                        base_arch = frozenset(Predicate.from_string_sieben(s) for s in z)
                        archs_to_use.append(base_arch)
                        if base_arch in master_archetypes.keys():
                            master_archetypes[base_arch].add((i, key))
                        else:
                            master_archetypes[base_arch] = {(i, key)}
    times=[]
    responsivities=[]
    interchangable = [
        ["b-x", "f-x", "m-x", "o-x", "s-x", "d-x", "eq-x"],
        ["b-y", "f-y", "m-y", "o-y", "s-y", "d-y", "eq-y"],
    ]
    archetypes=[]
    if searcher_name=="greedy":
        searcher=GreedySearcher(interchangable,max_depth=cutoff, beam=beam)
    else:
        searcher = BreadthSearcher(interchangable, max_depth=cutoff, beam=beam)
    for page in powerpoint.pages:
        start=datetime.now()
        slide=frozenset(Predicate.from_string_sieben(s) for s in page.RA)
        if equal_size:
            n = count_objects(slide)
            archs_to_use_per_slide = [
                archetype for archetype in archs_to_use if n == count_objects(archetype)
            ]
        else:
            archs_to_use_per_slide = archs_to_use.copy()
        result = searcher.search(slide,archs_to_use_per_slide)
        amount_placeholders=0
        best_archetype=None
        for res in result:
            moves=res[2]
            new_slide=slide.copy()
            for move in moves:
                new_slide=apply(new_slide,move)
            for solution in res[1]:
                archetype=archs_to_use_per_slide[solution]
                placeholders = len(similarity_optimal(archetype,slide)[1])
                if placeholders>amount_placeholders:
                    amount_placeholders=placeholders
                    best_archetype=list(master_archetypes[archetype])[0][0]
        responsivities.append(amount_placeholders/count_objects(slide))
        archetypes.append(best_archetype)
        times.append((datetime.now()-start).total_seconds())
    return list(zip(responsivities,archetypes,times))[0:5]



# def make_archetype(archetype,mapping):
#
#
#     #Titleslide
#     if archetype==0:
#         title_index = str(mapping[0])
#         subtext=[]
#         return TitleSlide(int(title_index),subtext)
#
#     #Title single content
#     elif archetype==1:
#         title_index = str(mapping[0])
#         single_content=str(mapping[1])
#         return TitleSingleContent(int(title_index),int(single_content))
#     #Title double content
#     elif archetype==2:
#         title_index=str(mapping[0])
#         double_content_1=str(mapping[1])
#         double_content_2=str(mapping[2])
#         return TitleDoubleContent(int(title_index),int(double_content_1),int(double_content_2))
#
#     #Title triple content
#     elif archetype==3:
#
#         title_index = str(mapping[0])
#         triple_content_1 = str(mapping[1])
#         triple_content_2 = str(mapping[2])
#         triple_content_3 = str(mapping[3])
#         return TitleTripleContent(int(title_index),int(triple_content_1),int(triple_content_2),int(triple_content_3))
#     #Comparison
#     elif archetype==4:
#         title_index = str(mapping[0])
#         double_content_1 = str(mapping[1])
#         double_content_2 = str(mapping[2])
#         double_subcontent_1=str(mapping[3])
#         double_subcontent_2 = str(mapping[4])
#
#         return Comparison(int(title_index), int(double_content_1), int(double_content_2), int(double_subcontent_1),int(double_subcontent_2))
#     #Section header
#     elif archetype==5:
#         title_index = str(mapping[0])
#         subtext = []
#         return SectionHeader(int(title_index), subtext)
#
#     #Title Only
#     elif archetype==6:
#         title_index = str(mapping[0])
#         return TitleOnly(int(title_index))
#     #Captioned Content
#     elif archetype==7:
#         left_up=str(mapping[0])
#         left_down=str(mapping[1])
#         right=str(mapping[2])
#         return CaptionedContent(int(left_up),int(left_down),int(right))
#     #Background Quote
#     elif archetype==8:
#         title=str(mapping[0])
#         background=str(mapping[1])
#         return BackgroundQuote(int(title),int(background))
#     #Background Only
#     elif archetype==9:
#         background=str(mapping[0])
#         return BackgroundOnly(int(background))
#
