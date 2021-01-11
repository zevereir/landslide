# from thesis_sieben_bocklandt.code.prototyping.pdf2xml import pdf2xml
# from thesis_sieben_bocklandt.code.prototyping.xml_preparse2tree import preparse_xml
# from thesis_sieben_bocklandt.code.prototyping.tree2features import tree2features
# from thesis_sieben_bocklandt.code.prototyping.tree2RA import tree2RA
# import xml.etree.ElementTree as ET
# pdf_file = "D:\\Thesis\\landslide\\possible_slides.pdf"
# output_directory = "D:\\Thesis\\landslide\\possible_slides_data"
# testing=False
# print("-->PDF2XML")
# xml_file = pdf2xml(pdf_file, output_directory)
# print("-->preparse_xml")
# xml_tree = preparse_xml(xml_file, output_directory)
# # print("-->xml2image")
# print("-->tree2features")
# feature_tree = tree2features(xml_tree, xml_file, output_directory, True)
# # print("-->xml2image")
# print("-->tree2RA")
# powerpoint, tree_with_indexes, one_background = tree2RA(feature_tree, xml_file)
# for i in powerpoint.pages:
#  print(i.RA)
from thesis_sieben_bocklandt.code.prototyping.RA2archetype import optimal_substitution
file1 = open('D:\\Thesis\\landslide\\sets.txt', 'r')
Lines = file1.readlines()
print(len(Lines))
# for i in Lines:
#  print(i)
archetypes=[6,6,6,18,54,72,2,6,2,1]
indices=   [2,2,2,3 ,4 ,5 ,1,3,2,1]
finalized=[]
for i in range(0,len(archetypes)):
 result=[]
 needed=Lines[sum(archetypes[0:i]):sum(archetypes[0:i])+archetypes[i]]
 for line in needed:
   already_in=False
   repr = set([x.strip().replace("'","") for x in line[1:-2].split(",")])
   for al in result:
     dis,sol,map=optimal_substitution(frozenset(repr),frozenset(al),indices[i],indices[i])
     if sol:
        already_in=True
        break
   if not already_in:
    result.append(repr)
 finalized.append(result)

#final results: [2,5,6,10,41,33,2,2,2,1]
for i in finalized:
 print(i)


 #print(set(len(line[1:-1].split(","))))

