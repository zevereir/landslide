import numpy as np
import itertools
POSITIONS = ["linksboven", "middelboven", "rechtsboven", "linksmiddel", "middelmiddel", "rechtsmiddel", "linksonder",
             "middelonder", "rechtsonder"]

RELATIONS=["b", "f", "m", "o", "s", "d", "eq", "di", "si", "oi", "mi", "fi", "bi"]


def RA_encoding(RA, title_indices):
    n=len(RA)
    encoding=set()
    for x in range(0,n):
        for y in range(0,n):
            relation=RA[x][y]
            if len(relation)==2:
                encoding.add(relation[0]+"-x+"+str(x)+"_"+str(y))
                encoding.add(relation[1] + "-y+" + str(x) + "_" + str(y))
            else:
                encoding.add(relation+"+"+str(x))
    for i in title_indices:
        encoding.add("title+"+str(i))
    return encoding,n

def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

def evaluate_mapping(enc,mapping):
    new_enc=set()
    for i in enc:
        if len(i)==2:
            new_tup=()
            for x in i:
                new_str = ""
                for letter in x:
                    if letter in mapping.keys():
                        new_str += mapping[letter]
                    else:
                        new_str += letter
                new_tup+=(new_str,)
            new_enc.add(new_tup)
        else:
            new_str=""
            for letter in i:
                if letter in mapping.keys():
                    new_str+=mapping[letter]
                else:
                    new_str+=letter
            new_enc.add(new_str)
    return new_enc

def get_mappings(enc1,enc2,n1,n2):
    mappings=[]
    range_1=range(0,n1)
    range_2=range(0,n2)
    title1=None
    title2 = None
    for i in range_1:
        if "title+"+str(i) in enc1:
            title1=i
        if "title+"+str(i) in enc2:
            title2=i
    permutations = list(itertools.permutations(range_1,n2))
    for perm in permutations:
        mapping={}
        for i in range_2:
            mapping[str(i)]=str(perm[i])
        mappings.append(mapping)
    if title1!=None and title2!=None:
        mappings=[x for x in mappings if x[str(title1)]==str(title2)]
    return mappings

def optimal_substitution(in_enc1,in_enc2,in_n1,in_n2):
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
    max_enc=enc2
    if max_dist==1.0:
        return enc1,enc2,1.0
    else:
        for mapping in get_mappings(enc1,enc2,n1,n2):
            new_enc=evaluate_mapping(enc2,mapping)
            new_jacard=jaccard(enc1,new_enc)
            if max_dist<new_jacard:
                max_dist=new_jacard
                max_enc=new_enc
            if max_dist==1.0:
                return enc1,new_enc,1.0
    return enc1,max_enc,max_dist


test=[["middelmiddel",("bi","b")],[("b","bi"),"middelonder"]]
test2=[["middelonder",("b","bi")],[("bi","b"),"middelmiddel"]]
titel_index=[0]
titel_index2=[1]
enc1,n1=RA_encoding(test,titel_index)
enc2,n2=RA_encoding(test2,titel_index2)
print(optimal_substitution(enc1,enc2,n1,n2))
