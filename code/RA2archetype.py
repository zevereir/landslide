import itertools
from functools import lru_cache
import json
from classes import *
from tree2RA import NOT_OVERLAPPING, OVERLAPPING
import globals as glob
from search import BreadthSearcher, GreedySearcher, count_objects, Predicate, similarity_optimal, apply
from datetime import datetime

def RA2archetype(powerpoint, arch_to_use, cutoff, equal_size, beam, searcher_name, single_content):
    """"
    De functie die een slideshow uitgedrukt in RA-algebra omzet naar archetypes.
    Deze archetypes zijn de basisvormen van de uiteindelijke powerpoint. Deze functie geeft archetype-objecten terug
    met daarin de juiste geanoteerde content_indexes die later samen met de categorized xml terug de slide kunnen opbouwen."""
    archs_to_use=[]
    master_archetypes = {}
    if arch_to_use=="baseline":
        with open('code/archetypes/baseline.json') as json_file:
            arch_dict = json.load(json_file)
        for i in range(0, len(arch_dict)): #archetype
            if (not single_content) or i in [1, 7, 9]:
                arch = arch_dict[str(i)]
                for key in arch: #master
                    master=arch[key]
                    for z in master:
                        base_arch = frozenset(Predicate.from_string_sieben(s) for s in z["Representation"])
                        mapping=z["Mapping"]
                        if base_arch not in archs_to_use:
                            archs_to_use.append(base_arch)
                        if base_arch in master_archetypes.keys():
                            master_archetypes[base_arch].append((i, key, mapping))
                        else:
                            master_archetypes[base_arch] = [(i, key, mapping)]

    elif arch_to_use=="learned":
        with open('code/archetypes/learned.json') as json_file:
            arch_dict = json.load(json_file)
        for i in range(0, len(arch_dict)): #archetype
            if (not single_content) or i in [1, 7, 9]:
                arch = arch_dict[str(i)]
                for key in arch: #master
                    master=arch[key]
                    for z in master:
                        base_arch = frozenset(Predicate.from_string_sieben(s) for s in z["Representation"])
                        mapping=z["Mapping"]
                        if base_arch not in archs_to_use:
                            archs_to_use.append(base_arch)
                            if base_arch in master_archetypes.keys():
                                master_archetypes[base_arch].append((i, key, mapping))
                            else:
                                master_archetypes[base_arch] = [(i, key, mapping)]
    elif arch_to_use=="masters":
        with open('code/archetypes/masters.json') as json_file:
            arch_dict = json.load(json_file)
        for i in range(0, len(arch_dict)):
            if (not single_content) or i in [1, 7, 9]:
                arch = arch_dict[str(i)]
                for key in arch: #master
                    master=arch[key]
                    for z in master:
                        base_arch = frozenset(Predicate.from_string_sieben(s) for s in z["Representation"])
                        mapping=z["Mapping"]
                        if base_arch not in archs_to_use:
                            archs_to_use.append(base_arch)
                        if base_arch in master_archetypes.keys():
                            master_archetypes[base_arch].append((i, key, mapping))
                        else:
                            master_archetypes[base_arch] = [(i, key, mapping)]

   
    times=[]
    responsivities=[]
    interchangable = [
        ["b-x", "f-x", "m-x", "o-x", "s-x", "d-x", "eq-x"],
        ["b-y", "f-y", "m-y", "o-y", "s-y", "d-y", "eq-y"],
    ]
    archetypes=[]
    if searcher_name=="greedy":
        searcher=GreedySearcher(interchangable,max_depth=cutoff, size=beam)
    else:
        searcher = BreadthSearcher(interchangable, max_depth=cutoff, size=beam)
    results={x:{} for x in range(1,len(powerpoint.pages)+1)}
    counter=0
    for page in list(powerpoint.pages):

        counter+=1

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
        amount_placeholders=-1
        best_archetype=None
        best_archetype_repr=None
        best_master=None
        best_new_slide=None
        best_mapping=None
        best_role_mapping=None
        best_moves=None
        for res in result:
            moves=res[2]
            new_slide=apply(slide, moves)
            for solution in res[1]:
                archetype=archs_to_use_per_slide[solution]
                mapping=similarity_optimal(new_slide,archetype)[1]
                placeholders = len(mapping)
                if placeholders>amount_placeholders:
                    amount_placeholders=placeholders
                    best_archetype=list(master_archetypes[archetype])[0][0]
                    best_archetype_repr=archetype
                    best_master=list(master_archetypes[archetype])[0][1]
                    best_role_mapping=list(master_archetypes[archetype])[0][2]
                    best_new_slide=new_slide
                    best_mapping=mapping
                    best_moves=moves
        responsivity=amount_placeholders/max(1,count_objects(slide))
        if responsivity<=0:
            best_archetype=11
            responsivity=0
        responsivities.append(responsivity)
        archetypes.append(best_archetype)
        duration=(datetime.now()-start).total_seconds()
        times.append(duration)
        current_result= {}
        current_result["Responsitivity"]=responsivity
        current_result["Time"]=duration
        current_result["New slide"]=str(best_new_slide)
        current_result["Archetype representation"]=str(best_archetype_repr)
        current_result["Archetype"]=best_archetype
        current_result["Master"]=best_master
        current_result["Best mapping"]=best_mapping
        current_result["Best role mapping"]=best_role_mapping
        current_result["Comparisons"]=searcher.comparisons
        current_result["Transformations"]=best_moves
        results[counter]=current_result

    return list(zip(responsivities,archetypes,times,)), results



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
