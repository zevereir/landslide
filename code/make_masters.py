from pdf2xml import pdf2xml
from xml_preparse2tree import preparse_xml
from tree2features import tree2features
from tree2RA import tree2RA
import xml.etree.ElementTree as ET
from search import similarity_optimal, Predicate, count_objects

removed_count=0
for ind in range(0,35):
    print(ind)
    index=str(ind)

    #MAKING CATEGORIZED XML
    pdf_file = "D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+".pdf"
    output_directory = "D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+"_data"
    testing=False
    print("-->PDF2XML")
    xml_file = pdf2xml(pdf_file, output_directory)
    print("-->preparse_xml")
    xml_tree = preparse_xml(xml_file, output_directory)
    # print("-->xml2image")
    print("-->tree2features")
    feature_tree = tree2features(xml_tree, xml_file, output_directory, True)

    #MAKING RA_REPR
    # feature_tree = ET.parse("D:\\Thesis\\landslide\\multiple_masters\\new_"+index+"_data\\new_"+index+"_categorized.xml")
    # xml_file="D:\\Thesis\\landslide\\multiple_masters\\new_"+index+"_data\\new_"+index+"_categorized.xml"
    # powerpoint, tree_with_indexes, one_background = tree2RA(feature_tree, xml_file)
    # f = open("D:\\Thesis\\landslide\\multiple_masters\\new_"+index+"_data\\set.txt", "w")
    # for i in powerpoint.pages:
    #     f.write(str(i.RA)+"\n")
    # f.close()

    #REMOVING DUPLICATES

#     file1 = open('D:\\Thesis\\landslide\\multiple_masters\\new_' + index + '_data\\set.txt', 'r')
#     Lines = file1.readlines()
#
#     archetypes=[6,6,18,54,162,6,2,18,2,1]
#     length_of_archetype=[2,2,3,4,5,2,1,3,2,1]
#     finalized=[]
#     line_count=0
#     total_lines=len(Lines)
#     for i in range(0,len(archetypes)):
#         result=[]
#         needed=Lines[sum(archetypes[0:i]):sum(archetypes[0:i+1])]
#         for line in needed:
#             line_count+=1
#             print(line_count,total_lines)
#             already_in=False
#             repr = set([x.strip().replace("'","") for x in line[1:-2].split(",")])
#             if i==0:
#                 repr.add("first_slide")
#             good_repr=frozenset(Predicate.from_string_sieben(s) for s in repr)
#             if count_objects(good_repr)==length_of_archetype[i]:
#                 for al in result:
#                     good_al=frozenset(Predicate.from_string_sieben(s) for s in al)
#                     sol,_=similarity_optimal(good_al,good_repr)
#                     if sol==1:
#                         already_in=True
#                         removed_count+=1
#                         break
#                 if not already_in:
#                     result.append(repr)
#             else:
#                 print("REMOVED BY COUNT", count_objects(good_repr))
#         finalized.append(result)
#     f = open("D:\\Thesis\\landslide\\multiple_masters\\new_"+index+"_data\\set_archetypes.txt", "w")
#     for i in finalized:
#         print(str(i))
#         f.write(str(i)+"\n\n")
#     f.close()
# print(removed_count)