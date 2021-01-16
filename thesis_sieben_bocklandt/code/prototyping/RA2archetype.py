import itertools
from functools import lru_cache
import json
from thesis_sieben_bocklandt.code.prototyping.classes import *
from thesis_sieben_bocklandt.code.prototyping.tree2RA import NOT_OVERLAPPING, OVERLAPPING
import thesis_sieben_bocklandt.code.prototyping.globals as glob
from datetime import datetime
# TITLE_SLIDE=({"title+0","first_slide"},1)
# TITLE_SINGLE_CONTENT=({"title+0","middelboven+0","bi-y+0_1","overlapping-x+0_1"},2)
# TITLE_DOUBLE_CONTENT=({"title+0","middelboven+0","bi-y+0_1","overlapping-x+0_1","bi-y+0_2","overlapping-y+1_2","not_overlapping-x+1_2"},3)
# TITLE_TRIPLE_CONTENT=({"title+0","middelboven+0","bi-y+0_1","overlapping-x+0_1","bi-y+0_2","bi-y+0_3","overlapping-y+1_2","overlapping-y+1_3","overlapping-y+2_3","not_overlapping-x+1_2","not_overlapping-x+1_3","not_overlapping-x+2_3"},4)
# COMPARISON=({"title+0","middelboven+0","bi-y+0_1","bi-y+0_2","bi-y+1_3","bi-y+2_4","overlapping-y+1_2","not_overlapping-x+1_2","overlapping-y+3_4","not_overlapping-x+3_4","overlapping-x+1_3","overlapping-x+2_4"},5)
# SECTION_HEADER=({"title+0","middelmiddel+0"},1)
# TITLE_ONLY=({"title+0","middelboven+0, no_content"},1)
# CAPTIONED_CONTENT=({"bi-y+0_1","overlapping-x+0_1","not_overlapping-x+0_2","not_overlapping-x+1_2","overlapping-y+0_2","overlapping-y+1_2","no_title"},3)
# BACKGROUND_QUOTE=({"title+0","middelmiddel+0","background+1"},2)
# BACKGROUND_ONLY=({"background+0","no_title"},1)
# ARCHETYPES=[TITLE_SLIDE,TITLE_SINGLE_CONTENT,TITLE_DOUBLE_CONTENT,TITLE_TRIPLE_CONTENT,COMPARISON,SECTION_HEADER,TITLE_ONLY,CAPTIONED_CONTENT,BACKGROUND_QUOTE,BACKGROUND_ONLY]
# NAMES=["TITLE_SLIDE","TITLE_SINGLE_CONTENT","TITLE_DOUBLE_CONTENT","TITLE_TRIPLE_CONTENT","COMPARISON","SECTION_HEADER","TITLE_ONLY","CAPTIONED_CONTENT","BACKGROUND_QUOTE","BACKGROUND_ONLY"]

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]


def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    return float(intersection) / max((len(list1) + len(list2)) - intersection,1)

def evaluate_mapping(enc,mapping):
    new_enc=set()
    for i in enc:
        if i=="first_slide" or i=="no_title" or i=="no_content":
            new_enc.add(i)
        else:
            plus_index=i.index("+")+1
            numbers=i[plus_index:]
            if "_" in numbers:
                line_index=numbers.index("_")
                number1=numbers[:line_index]
                number2=numbers[line_index+1:]

                if int(number1) not in mapping.keys():
                    mapping[int(number1)]=number1
                if int(number2) not in mapping.keys():
                    mapping[int(number2)]=number2
                new_enc.add(i[:plus_index]+mapping[int(number1)]+"_"+mapping[int(number2)])
            else:
                if int(numbers) not in mapping.keys():
                    mapping[int(numbers)]=numbers
                new_enc.add(i[:plus_index] + mapping[int(numbers)])
    return new_enc

def get_mappings(title1,title2,n1,n2):
    mappings=[]
    range_1=range(0,n1)
    permutations = list(itertools.permutations(range_1,n2))
    for perm in permutations:
        mapping={}
        for i in range(0,n2):
            mapping[str(i)]=str(perm[i])
        mappings.append(mapping)
    if title1!=None and title2!=None:
        mappings=[x for x in mappings if x[str(title2)]==str(title1)]
    return mappings


def get_full_mappings(enc1,enc2,n1,n2, equal):
    possibilities={}
    possibilities2={}
    for i in enc2:
        if "first_slide" not in i and "no_content" not in i and "no_title" not in i:
            z = ''.join([x for x in i if not x.isdigit()])[:-1]

            if "_" in i:
                numbers=i[-len(i)+len(z):].split("_")
                x1=int(numbers[0])
                x2=int(numbers[1])
                if z in possibilities.keys():
                    possibilities[z].append((x1,x2))
                else:
                    possibilities[z]=[((x1,x2))]
            else:
                numbers = int(i[-len(i) + len(z):])
                if z in possibilities.keys():
                    possibilities[z].append((numbers,))
                else:
                    possibilities[z]=[(numbers,)]
    for i in enc1:
        if "first_slide" not in i and "no_content" not in i and "no_title" not in i:

            z = ''.join([x for x in i if not x.isdigit()])[:-1]

            if "_" in i:
                numbers = i[-len(i) + len(z):].split("_")
                x1 = alphabet[int(numbers[0])]
                x2 = alphabet[int(numbers[1])]
                if z in possibilities2.keys():
                    possibilities2[z].append((x1, x2))
                else:
                    possibilities2[z] = [((x1, x2))]
            else:
                numbers = alphabet[int(i[-len(i) + len(z):])]
                if z in possibilities2.keys():
                    possibilities2[z].append((numbers,))
                else:
                    possibilities2[z] = [(numbers,)]
    possible_combinations={}
    for i in possibilities.keys()&possibilities2.keys():
        val1=possibilities[i]
        val2=possibilities2[i]
        x1=set([x[0] for x in val1])
        x2=set([x[0] for x in val2])
        for comb in list(itertools.product(x1,x2)):
            if comb[0] in possible_combinations.keys():
                possible_combinations[comb[0]].add(comb[1])
            else:
                possible_combinations[comb[0]]={comb[1]}

        if len(val1[0])>1:
            y1 = set([x[1] for x in val1])
            y2 = set([x[1] for x in val2])
            for comb in list(itertools.product(y1,y2)):

                if comb[0] in possible_combinations.keys():
                    possible_combinations[comb[0]].add(comb[1])
                else:
                    possible_combinations[comb[0]] = {comb[1]}
    #("POSSIBLE COMBINATIONS",possible_combinations)
    mapping={}
    changes=True
    while changes:
        changes=False
        for i in possible_combinations.keys():
            if len(possible_combinations[i])==1:
                changes=True
                mapping[i]=(possible_combinations.pop(i)).pop()
                for x in possible_combinations.keys():
                    if mapping[i] in possible_combinations[x]:
                        possible_combinations[x].remove(mapping[i])
                break;
    rest_pos=[]
    for i in possible_combinations.keys():
        rest_pos.append(list(itertools.product({i},possible_combinations[i])))
    all_combinations=list(itertools.product(*rest_pos))
    new_mappings=[]
    for w in all_combinations:
        p = {j[1] for j in w}
        if len(p) == len(w):
            current_mapping=mapping.copy()
            for z in w:
                current_mapping[z[0]]=z[1]
            new_mappings.append(current_mapping)
    result=[]
    if equal:
        for p in new_mappings:
            if len(p.keys())==n2:
                result.append(p)
    else:
        result=new_mappings

    glob.numb_mappings+=len(result)
    glob.count_mappings+=1
    return result



@lru_cache(maxsize=None, typed=False)
def optimal_substitution(in_enc1,in_enc2,in_n1,in_n2, equal_size, subset):
    glob.numb_substitution+=1
    #enc1 is always the longest
    if in_n1>=in_n2:
        enc1=in_enc1
        enc2=in_enc2
        n1=in_n1
        n2=in_n2
    else:
        enc1=in_enc2
        enc2=in_enc1
        n1 = in_n2
        n2 = in_n1
    max_dist=jaccard(enc1,enc2)
    mapping_standard={}
    for i in range(0,n1):
        mapping_standard[i]=i
    #print("STANDARD",mapping_standard)
    if max_dist==1.0:
        return 1.0,True,mapping_standard
    # elif in_n2<=in_n1 and jaccard(enc2,enc1&enc2)==1.0:
    #     return max_dist,True,mapping_standard
    else:
        best_mapping=mapping_standard
        # title1=None
        # title2=None
        # for i in range(0,n1):
        #     if "title+"+str(i) in enc1:
        #         title1=i
        #     if "title+"+str(i) in enc2:
        #         title2=i
        all_mappings=get_full_mappings(frozenset(enc1),frozenset(enc2),n1,n2, equal_size and not subset)

        #print("ALL_MAPPINGS",all_mappings)
        new_enc_1=set()
        for i in enc1:
            if "first_slide" not in i and "no_content" not in i and "no_title" not in i:
                z = ''.join([x for x in i if not x.isdigit()])[:-1]
                if "_" in i:
                    numbers = i[-len(i) + len(z):].split("_")
                    x1 = alphabet[int(numbers[0])]
                    x2 = alphabet[int(numbers[1])]
                    new_enc_1.add(i[:-len(i) + len(z)]+x1+"_"+x2)
                else:
                    numbers = alphabet[int(i[-len(i) + len(z):])]
                    new_enc_1.add(i[:-len(i) + len(z)+1] + numbers)

        for mapping in all_mappings:#get_mappings(title1,title2,n1,n2):
            if len(mapping)!=0:
                if mapping!=mapping_standard:
                    #print("MAPPING BEFORE",mapping)
                    new_enc=evaluate_mapping(enc2,mapping)
                    #print("MAPPING AFTER", mapping)
                    new_jacard=jaccard(new_enc_1,new_enc)
                    if max_dist<new_jacard:
                        #print("NEW BEST MAPPING",mapping)
                        max_dist=new_jacard
                        best_mapping=mapping

                    if max_dist==1.0:# or (in_n2<=in_n1 and jaccard(new_enc,enc1&new_enc)==1.0):
                        if n1>n2:

                            reversed_mapping = {}
                            for i in mapping.keys():
                                if mapping[i] in alphabet:
                                    reversed_mapping[alphabet.index(mapping[i])] = i
                            for i in range(0, n1):
                                if i not in reversed_mapping.keys():
                                    reversed_mapping[i] = len(reversed_mapping)
                            mapping = reversed_mapping
                        else:
                            # print("normal")
                            for i in mapping.keys():
                                if mapping[i] in alphabet:
                                    mapping[i] = alphabet.index(mapping[i])

                        return max_dist, True,mapping
    #print("OP_MAPPING",best_mapping)

    if n1 > n2:
        #print("Reverse")

        reversed_mapping = {}
        for i in best_mapping.keys():
            if best_mapping[i] in alphabet:
                reversed_mapping[alphabet.index(best_mapping[i])] = i
        for i in range(0, n1):
            if i not in reversed_mapping.keys():
                reversed_mapping[i] = len(reversed_mapping)
        best_mapping = reversed_mapping
    else:
        #print("normal")
        for i in best_mapping.keys():
            if best_mapping[i] in alphabet:
                best_mapping[i] = alphabet.index(best_mapping[i])
    #print("Best_mapping",best_mapping)
    return max_dist,False, best_mapping


def RA2archetype(powerpoint, arch_to_use, cutoff, equal_size, beam):
    indices = [1,1,2,3,4,1,0,2,1,0]
    """"
    De functie die een slideshow uitgedrukt in RA-algebra omzet naar archetypes.
    Deze archetypes zijn de basisvormen van de uiteindelijke powerpoint. Deze functie geeft archetype-objecten terug
    met daarin de juiste geanoteerde content_indexes die later samen met de categorized xml terug de slide kunnen opbouwen."""
    archs_to_use=[]
    if arch_to_use=="baseline":
        with open('thesis_sieben_bocklandt/code/prototyping/archetypes/baseline.json') as json_file:
            arch_dict = json.load(json_file)
        for i in range(0, len(arch_dict)):
            archs_to_use.append(([frozenset(v) for v in arch_dict[str(i)]],indices[i]+1))
    # elif arch_to_use=="overlap":
    #     archs_to_use=[([x[0]],x[1]) for x in ARCHETYPES]
    elif arch_to_use=="learned":
        with open('thesis_sieben_bocklandt/code/prototyping/archetypes/learned.json') as json_file:
            arch_dict = json.load(json_file)
        for i in range(0, len(arch_dict)):
            master = arch_dict[str(i)]
            archs = []
            for key in range(0, len(master)):
                for z in master[str(key)]:
                    if frozenset(z) not in archs:
                        archs.append(frozenset(z))
                archs_to_use.append((archs, indices[i] + 1))
    elif arch_to_use=="masters":
        master_archetypes=[]
        mapping_archetypes={}

        with open('thesis_sieben_bocklandt/code/prototyping/archetypes/multiple_masters.json') as json_file:
            arch_dict=json.load(json_file)
        for i in range(0,len(arch_dict)):
            archs = []
            for key in range(0,len(arch_dict["0"])):
                if key!=25:
                    master=arch_dict[str(i)][str(key)]
                    for z in master:
                        if frozenset(z) not in archs:
                            archs.append(frozenset(z))
                        if frozenset(z) in mapping_archetypes.keys():
                            mapping_archetypes[frozenset(z)].add(int(key))
                        else:
                            mapping_archetypes[frozenset(z)]={int(key)}
            archs_to_use.append((archs,indices[i]+1))

    archetypes=[]
    times=[]
    total_pages=len(powerpoint.pages)
    count=1
    glob.init_count()
    for page in powerpoint.pages:
        start=datetime.now()
        glob.init()
        possible_archetypes,simil= find_archetype(page.RA,page.n, True,archs_to_use,equal_size, cutoff,beam=beam)
        times.append((datetime.now()-start).total_seconds())
        #print("Dia",count,"#iteraties=",glob.numb_iterations, "#substituties=", glob.numb_substitution)
        count += 1
        if arch_to_use!="masters":
            try:
                x=len(possible_archetypes[0][0])
                archetypes.append(possible_archetypes[0][0][0])
            except:
                archetypes.append(possible_archetypes[0][0])
            #print(possible_archetypes[0][0])
        else:
            master_archetypes.append(possible_archetypes)
    if arch_to_use=="masters":
        counts={}
        for i in range(0,len(arch_dict["0"])):
            counts[i]=0
        for ma in master_archetypes:
            for pos in ma:
                try:
                    if pos[1]!=frozenset():
                        for belongs_to in mapping_archetypes[pos[1]]:
                            counts[belongs_to]+=1
                except:
                    if pos[0][1] != frozenset():
                        for belongs_to in mapping_archetypes[pos[1]]:
                            counts[belongs_to] += 1
        for ma in master_archetypes:
            best_arch=None
            best_score=-1
            for pos in ma:
                try:
                    if pos[1] == frozenset():
                        best_arch = pos[0]
                    else:
                        best_map=max([counts[v] for v in mapping_archetypes[pos[1]]])
                        if best_map>best_score:
                            best_arch=pos[0]
                except:
                    if pos[0][1] == frozenset():
                        best_arch = pos[0][0]
                    else:
                        best_map=max([counts[v] for v in mapping_archetypes[pos[0][1]]])
                        if best_map>best_score:
                            best_arch=pos[0][0]
            try:
                x=len(best_arch)
                archetypes.append(best_arch[0])
            except:
                archetypes.append(best_arch)
    #print("Gemiddelde mappings",glob.numb_mappings,glob.count_mappings, glob.numb_mappings/glob.count_mappings)
    return archetypes,[], times

def remove_overlapping(RA_set):
    n=RA_set[1]
    RA_list=list(RA_set[0])
    lists=[RA_list]
    while "overlapping" in str(lists[0]):
        new_lists=[]
        for lijst in lists:
            index = [idx for idx, s in enumerate(lijst) if 'overlapping' in s][0]
            el = lijst.pop(index)
            if el.startswith("not_overlapping"):
                numbers=el[15:]
                for rel in NOT_OVERLAPPING:
                    new_lists.append(lijst+[rel+numbers])
            else:
                numbers = el[11:]
                for rel in OVERLAPPING:
                    new_lists.append(lijst+[rel+numbers])
        lists=new_lists[:]
    return [(set(l),n) for l in lists]

def find_archetype(RA,n, recursive, archs_to_use,equal_size, cutoff=0, subset=False, beam=None):
    """"
    De functie die voor een bepaalde slide (gegeven door de RA-matrix) het archetype bepaald. Dit gaat als volgt:
    1. er worden een aantal constraints bepaald
    2. Als een slide een een correcte combinatie van constraints voldoet is het dat archetype
    3. als dit niet het geval is wordt er via een breadth-first-search een nieuwe RA opgesteld waarvoor terug een archetype gezocht wordt"""
    best_simil=0
    best_archetype=None
    best_mapping=None
    glob.numb_iterations+=1
    if n>8:
        return [(ContentOnly(range(0,n)),frozenset())],0
    solutions=[]
    best_dist=0
    best_arch=None
    for index in range(0,len(archs_to_use)):
        #remove_overlapping(ARCHETYPES[index]):
        archie = archs_to_use[index]
        archetype=archie[0]
        archetype_length=archie[1]
        if ((not equal_size or subset) and n>=archetype_length) or archetype_length==n:
            for arch in archetype:
                dist,solution,mapping=optimal_substitution(frozenset(RA),frozenset(arch),n,archetype_length, equal_size,subset)
                if not subset and solution:
                    solutions.append((make_archetype(index,n,mapping, RA),arch))
                    break;
                elif subset and dist>best_dist:
                    #print("mapping",mapping)
                    best_dist=dist
                    best_arch=[(make_archetype(index,n,mapping, RA),arch)]
    if (not equal_size or subset) and best_arch!=None:
        return best_arch,best_dist
    elif subset:
        return [[(ContentOnly(range(0,n)),frozenset())]],0
    if solutions!=[]:
        return solutions,1
    elif recursive:
        solutions=select_closest(RA,n, archs_to_use, cutoff, equal_size, beam)

        return solutions[0],1
    else:
        return None,0
def make_archetype(archetype,n,mapping, RA):
    reversed_mapping={}
    for i in mapping.keys():
        reversed_mapping[mapping[i]]=i
    #Titleslide
    if archetype==0:
        title_index = str(reversed_mapping[0])
        subtext=[]
        return TitleSlide(int(title_index),subtext)

    #Title single content
    elif archetype==1:
        title_index = str(reversed_mapping[0])
        single_content=str(reversed_mapping[1])
        return TitleSingleContent(int(title_index),int(single_content))
    #Title double content
    elif archetype==2:
        title_index=str(reversed_mapping[0])
        double_content_1=str(reversed_mapping[1])
        double_content_2=str(reversed_mapping[2])
        if "b-x+"+double_content_1+"_"+double_content_2 in RA or "m-x+"+double_content_1+"_"+double_content_2 in RA:
            return TitleDoubleContent(int(title_index),int(double_content_1),int(double_content_2))
        else:
            return TitleDoubleContent(int(title_index),int(double_content_2),int(double_content_1))
    #Title triple content
    elif archetype==3:

        title_index = str(reversed_mapping[0])
        triple_content_1 = str(reversed_mapping[1])
        triple_content_2 = str(reversed_mapping[2])
        triple_content_3 = str(reversed_mapping[3])
        permutations = set(itertools.permutations([triple_content_1,triple_content_2,triple_content_3]))
        for i in permutations:
            if ("b-x+" + i[0] + "_" + i[1] in RA or "m-x+" + i[0] + "_" + i[1] in RA) and ("b-x+" + i[1] + "_" + i[2] in RA or "m-x+" + i[1] + "_" + i[2] in RA):
                return TitleTripleContent(int(title_index), int(i[0]), int(i[1]),int(i[2]))
        return TitleTripleContent(int(title_index),int(triple_content_1),int(triple_content_2),int(triple_content_3))
    #Comparison
    elif archetype==4:
        title_index = str(reversed_mapping[0])
        double_content_1 = str(reversed_mapping[1])
        double_content_2 = str(reversed_mapping[2])
        double_subcontent_1=str(reversed_mapping[3])
        double_subcontent_2 = str(reversed_mapping[4])
        if "b-x+" + double_content_1 + "_" + double_content_2 in RA or "m-x+" + double_content_1 + "_" + double_content_2 in RA:
            if "b-x+" + double_subcontent_1 + "_" + double_subcontent_2 in RA or "m-x+" + double_subcontent_1 + "_" + double_subcontent_2 in RA:
                return Comparison(int(title_index), int(double_content_1), int(double_content_2), int(double_subcontent_1),int(double_subcontent_2))
            else:
                return Comparison(int(title_index), int(double_content_1), int(double_content_2), int(double_subcontent_2),int(double_subcontent_1))
        else:
            if "b-x+" + double_subcontent_1 + "_" + double_subcontent_2 in RA or "m-x+" + double_subcontent_1 + "_" + double_subcontent_2 in RA:
                return Comparison(int(title_index), int(double_content_2), int(double_content_1), int(double_subcontent_1),int(double_subcontent_2))
            else:
                return Comparison(int(title_index), int(double_content_2), int(double_content_1), int(double_subcontent_2),int(double_subcontent_1))
    #Section header
    elif archetype==5:
        title_index = str(reversed_mapping[0])
        subtext = []
        return SectionHeader(int(title_index), subtext)

    #Title Only
    elif archetype==6:
        title_index = str(reversed_mapping[0])
        return TitleOnly(int(title_index))
    #Captioned Content
    elif archetype==7:
        left_up=str(reversed_mapping[0])
        left_down=str(reversed_mapping[1])
        right=str(reversed_mapping[2])
        return CaptionedContent(int(left_up),int(left_down),int(right))
    #Background Quote
    elif archetype==8:
        title=str(reversed_mapping[0])
        background=str(reversed_mapping[1])
        return BackgroundQuote(int(title),int(background))
    #Background Only
    elif archetype==9:
        background=str(reversed_mapping[0])
        return BackgroundOnly(int(background))

def change_overlapping(relation):
    """functie die gebruik makend van een bepaalde relatie de switch maakt voor de breadth first search"""
    if relation =="middelboven":
        return "middelboven"
    elif relation =="middelmiddel":
        return "middelmiddel"
    elif relation in ["linksboven","rechtsboven"]:
        return "middelboven"
    elif relation in ["linksmiddel","rechtsmiddel","linksonder","middelonder","rechtsonder"]:
        return "middelmiddel"
    elif relation=="overlapping":
        return "not_overlapping"
    elif relation=="not_overlapping":
        return "overlapping"
    else:
        if relation in NOT_OVERLAPPING:
            if "i" not in relation:
                return "di"
            else:
                return "d"
        else:
            if "i" not in relation:
                return "bi"
            else:
                return "b"

def change_overlapping_full(all_changes,combo,new_RA, amount, archs, cutoff, equal_size, beam_change):

    positions = ["middelmiddel", "middelboven", "rechtsboven", "rechtsmiddel", "rechtsonder", "middelonder",
                 "linksonder", "linksmiddel", "linksboven"]
    relations = ["b", "m", "o", "d", "s", "f", "eq"]#, "fi", "si", "di", "oi", "mi", "bi"]
    binary_indices_to_change=[]
    for i in range(0,len(new_RA)):
        relation=new_RA[i]
        if "background" not in relation and "title" not in relation and "content" not in relation and "first_slide" not in relation:
            numbers = relation[relation.find("+") + 1:]
            change_1 = int(numbers[:numbers.find("_")])
            change_2 = int(numbers[numbers.find("_") + 1:])
            if (change_1, change_2) in all_changes or (change_2, change_1) in all_changes:
                if (change_1, change_2) in all_changes:
                    z = combo[all_changes.index((change_1, change_2))]
                else:
                    z = combo[all_changes.index((change_2, change_1))]
                if z % 2 == 0 and "-x" in relation:
                    binary_indices_to_change.append(i)
                if z > 0 and "-y" in relation:
                    binary_indices_to_change.append(i)
    combinations=[]
    # for i in single_indices_to_change:
    #     combinations.append([(i,x) for x in range(0,9) if x!=positions.index(new_RA[i][:-2])])
    for i in binary_indices_to_change:
        combinations.append([(i,x) for x in range(0,7) if x!=relations.index(new_RA[i][:new_RA[i].index("+")-2])])
    best_simil=0
    best_arch=None
    best_change=None
    solutions=[]
    for change in itertools.product(*combinations):

        if (beam_change!=[] and set(beam_change).issubset(set(change))) or beam_change==[]:
            #print("CHANGE",change)
            z=new_RA[:]
            for i in change:
                element=new_RA[i[0]]
                if "_" in element:
                    z[i[0]]=relations[i[1]]+element[element.index("-"):]
                else:
                    z[i[0]] = positions[i[1]] + +element[element.index("+"):]


            archetype,simil = find_archetype(set(z), amount, False, archs,equal_size, cutoff, True)
            if simil>best_simil:
                best_simil=simil
                best_arch=archetype
                best_change=change
            if simil==1:
                solutions.append(archetype)
    if solutions!=[]:
        return solutions,1,[]
    return best_arch,best_simil, best_change

from datetime import datetime
def select_closest(RA_set,amount, archs, cutoff, equal_size,beam):


    """
   Iterative deepening op de RA-matrix
    """
    #aantal elementen in de bovendriehoeksmatrix
    if amount>5:
        return find_archetype(RA_set, amount, False, archs, False, cutoff, True)
    max_amount_changes = int(amount + (amount * amount - amount) / 2)
    extra = 0
    mapping = {}
    #mapping van single getal naar extra getal om bovendriehoek om te zetten
    for i in range(0, max_amount_changes):
        if (i + sum(range(0, extra + 1))) % amount == 0 and i > 0:
            extra += 1
        mapping[i] = extra
    best_changes=[]
    beam_search=[]
    for amount_changes in range(1, max_amount_changes+1):
        if amount_changes>cutoff:
            return find_archetype(RA_set,amount,False,archs,equal_size,cutoff,True)
        #alle combinaties om linker, rechter en beide relaties om te zetten: bvb:
        combinations = [z for v in [set(itertools.permutations(x)) for x in
                                    list(itertools.combinations_with_replacement(range(0, 3), amount_changes))] for z in
                        v]
        possible_changes=list(set(itertools.combinations(range(0, max_amount_changes), amount_changes)))
        best_simil=0
        best_arch=None

        for changes_index in range(0,len(possible_changes)):
            changes=possible_changes[changes_index]
            all_changes = []
            for change in changes:
                extra = sum(range(0, mapping[change] + 1))
                x_index = (change + extra) // amount
                y_index = (change + extra) % amount
                all_changes.append((x_index, y_index))
            remove_same = [x for x in all_changes if x[0] == x[1]]
            if len(remove_same)==0:
                valid_beam = beam_search == []
                beam_change=[]
                if beam != None and beam_search != []:
                    for beam_changes in beam_search:
                        if (set(beam_changes[0]).issubset(set(all_changes))):
                            beam_change=beam_changes[1]
                            valid_beam = True
                            break;
                if beam==None or (beam!=None and valid_beam):

                    for combo in combinations:
                        # resolve 1 combination of changes
                        new_RA = list(RA_set)[:]
                        archetype, simil, best_change=change_overlapping_full(all_changes,combo,new_RA,amount, archs,cutoff,equal_size, beam_change)
                        if simil==1:
                            return archetype[0],simil
                        if (simil,all_changes, best_change) not in best_changes:
                            best_changes.append((simil,all_changes, best_change))
                        if simil>=best_simil and archetype!=None:
                            best_simil=simil
                            best_arch=archetype
        if beam!=None:
            beam_search = sorted(best_changes)
            beam_search.reverse()
            if len(beam_search)>=beam:
                beam_search=[(x[1],x[2]) for x in beam_search[0:beam]]
            else:
                beam_search=[(x[1],x[2]) for x in beam_search]

        # if best_arch!=None:
        #     return best_arch,best_simil
                # for i in range(0, len(new_RA)):
                #     relation = new_RA[i]
                #     if "background" not in relation and "title" not in relation and "content" not in relation and "first_slide" not in relation:
                #         numbers=relation[relation.find("+")+1:]
                #         if "_" not in numbers:
                #             single_change=int(numbers)
                #             if (single_change,single_change) in all_changes:
                #                 new_RA[i]=change_overlapping(relation[:-2])+relation[-2:]
                #         else:
                #             change_1=int(numbers[:numbers.find("_")])
                #             change_2 = int(numbers[numbers.find("_")+1:])
                #
                #             if (change_1,change_2) in all_changes or (change_2,change_1) in all_changes:
                #                 skip=relation.find("-")
                #                 if (change_1, change_2) in all_changes:
                #                     z=combo[all_changes.index((change_1, change_2))]
                #                 else:
                #                     z = combo[all_changes.index((change_2, change_1))]
                #                 if z % 2 == 0 and "-x" in relation:
                #                     new_RA[i]=change_overlapping(relation[:skip])+relation[skip:]
                #                 if z > 0 and "-y" in relation:
                #                     new_RA[i] = change_overlapping(relation[:skip]) + relation[skip:]
                # archetype = find_archetype(set(new_RA), amount, False)
                # if archetype!=None:
                #     # with open("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\clustering\\clusters.txt",'a') as f:
                #     #     if len(RA_set)>0:
                #     #         f.write(str((RA_set,amount))+"\n")
                #     return archetype
    # with open("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\clustering\\clusters.txt",'a') as f:
    #     if len(RA_set) > 0:
    #         f.write(str((RA_set, amount)) + "\n")

    return find_archetype(RA_set,amount,False,archs,equal_size,cutoff,True)


