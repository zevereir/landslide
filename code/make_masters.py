from pdf2xml import pdf2xml
from xml_preparse2tree import preparse_xml
from tree2features import tree2features
from tree2RA import tree2RA
import xml.etree.ElementTree as ET
from search import similarity_optimal, Predicate, count_objects
import json
masters={x:{} for x in range(0,10)}
removed_count=0

for ind in range(0,35):
    print(ind)
    index=str(ind)
    # #
    # # #MAKING CATEGORIZED XML
    # pdf_file = "D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+".pdf"
    # output_directory = "D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+"_data"
    # testing=False
    # print("-->PDF2XML")
    # xml_file = pdf2xml(pdf_file, output_directory)
    # print("-->preparse_xml")
    # xml_tree = preparse_xml(xml_file, output_directory)
    # # print("-->xml2image")
    # print("-->tree2features")
    # feature_tree = tree2features(xml_tree, xml_file, output_directory, True)

    #MAKING RA_REPR
    # feature_tree = ET.parse("D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+"_data\\new_"+index+"_categorized.xml")
    # xml_file="D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+"_data\\new_"+index+"_categorized.xml"
    # powerpoint, tree_with_indexes, one_background = tree2RA(feature_tree, xml_file)
    # f = open("D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+"_data\\set.txt", "w")
    # counter=0
    # for i in powerpoint.pages:
    #     if 0<counter<6:
    #         v=i.RA
    #         v.add("first_slide")
    #         f.write(str(v)+"\n")
    #
    #     else:
    #         f.write(str(i.RA)+"\n")
    #     counter+=1
    # f.close()

    #MAKING ALIGNMENTS FOR MASTERS
    # feature_tree = ET.parse("D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+"_data\\new_"+index+"_categorized.xml")
    # archetypes=[6,6,18,54,162,6,2,18,2,1]
    # counter=0
    # mappings=[]
    # for page in feature_tree.getroot():
    #     mapping={}
    #     if counter<6:
    #         for element in page:
    #             if element.text!=None:
    #                 if element.text.startswith("A"):
    #                     mapping[element.attrib.get("id")]="Title"
    #                 if element.text.startswith("B"):
    #                     mapping[element.attrib.get("id")]="Subtitle"
    #     elif counter<12:
    #         for element in page:
    #             if element.text!=None:
    #                 if element.text.startswith("A"):
    #                     mapping[element.attrib.get("id")]="Title"
    #                 if element.text.startswith("B"):
    #                     mapping[element.attrib.get("id")]="Content"
    #     elif counter<30:
    #         for element in page:
    #             if element.text!=None:
    #                 if element.text.startswith("A"):
    #                     mapping[element.attrib.get("id")]="Title"
    #                 if element.text.startswith("B"):
    #                     mapping[element.attrib.get("id")]="Left Content"
    #                 if element.text.startswith("C"):
    #                     mapping[element.attrib.get("id")]="Right Content"
    #     elif counter<84:
    #         for element in page:
    #             if element.text!=None:
    #                 if element.text.startswith("A"):
    #                     mapping[element.attrib.get("id")]="Title"
    #                 if element.text.startswith("B"):
    #                     mapping[element.attrib.get("id")]="Left Content"
    #                 if element.text.startswith("C"):
    #                     mapping[element.attrib.get("id")]="Middle Content"
    #                 if element.text.startswith("D"):
    #                     mapping[element.attrib.get("id")]="Right Content"
    #     elif counter<246:
    #         for element in page:
    #             if element.text!=None:
    #                 if element.text.startswith("A"):
    #                     mapping[element.attrib.get("id")]="Title"
    #                 if element.text.startswith("B"):
    #                     mapping[element.attrib.get("id")]="Left Subtitle"
    #                 if element.text.startswith("C"):
    #                     mapping[element.attrib.get("id")]="Right Subtitle"
    #                 if element.text.startswith("D"):
    #                     mapping[element.attrib.get("id")]="Left Content"
    #                 if element.text.startswith("E"):
    #                     mapping[element.attrib.get("id")]="Right Content"
    #     elif counter<252:
    #         for element in page:
    #             if element.text!=None:
    #                 if element.text.startswith("A"):
    #                     mapping[element.attrib.get("id")]="Title"
    #                 if element.text.startswith("B"):
    #                     mapping[element.attrib.get("id")]="Subtitle"
    #     elif counter<254:
    #         for element in page:
    #             if element.text!=None:
    #                 if element.text.startswith("A"):
    #                     mapping[element.attrib.get("id")]="Title"
    #     elif counter<272:
    #         for element in page:
    #             if element.text!=None:
    #                 if element.text.startswith("A"):
    #                     mapping[element.attrib.get("id")]="Left Subtitle"
    #                 if element.text.startswith("B"):
    #                     mapping[element.attrib.get("id")]="Left Content"
    #                 if element.text.startswith("C"):
    #                     mapping[element.attrib.get("id")]="Right Content"
    #     elif counter<274:
    #         for element in page:
    #             if element.text!=None:
    #                 if element.text.startswith("A"):
    #                     mapping[element.attrib.get("id")]="Title"
    #     else:
    #         pass
    #     mappings.append(mapping)
    #     counter+=1
    # f = open("D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+"_data\\mappings.txt", "w")
    # for mapping in mappings:
    #     f.write(str(mapping)+"\n")
    # f.close()

#     #REMOVING DUPLICATES
# #
#     file1 = open('D:\\Thesis\\landslide\\new_multiple_masters\\new_' + index + '_data\\set.txt', 'r')
#     Lines = file1.readlines()
#     file2 = open('D:\\Thesis\\landslide\\new_multiple_masters\\new_' + index + '_data\\mappings.txt', 'r')
#     Lines2 = file2.readlines()
#     print("LEN1",len(Lines))
#
#     archetypes=[6,6,18,54,162,6,2,18,2,1]
#     length_of_archetype=[2,2,3,4,5,2,1,3,2,1]
#     finalized=[]
#     line_count=0
#     total_lines=len(Lines)
#     for i in range(0,len(archetypes)):
#         result=[]
#         needed=Lines[sum(archetypes[0:i]):sum(archetypes[0:i+1])]
#         needed2=Lines2[sum(archetypes[0:i]):sum(archetypes[0:i+1])]
#         for line_ind in range(0,len(needed)):
#             line=needed[line_ind]
#             line2=needed2[line_ind]
#             line_count+=1
#             print(line_count,total_lines)
#             already_in=False
#             repr = set([x.strip().replace("'","") for x in line[1:-2].split(",")])
#             good_repr=frozenset(Predicate.from_string_sieben(s) for s in repr)
#             if count_objects(good_repr)==length_of_archetype[i]:
#                 for al in result:
#                     good_al=frozenset(Predicate.from_string_sieben(s) for s in al[0])
#                     sol,_=similarity_optimal(good_al,good_repr)
#                     if sol==1:
#                         already_in=True
#                         removed_count+=1
#                         break
#                 if not already_in:
#                     result.append((repr,line2))
#             else:
#                 print("REMOVED BY COUNT", count_objects(good_repr))
#         finalized.append(result)
#     f = open("D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+"_data\\set_archetypes.txt", "w")
#     for i in finalized:
#         print(str(i))
#         f.write(str(i)+"\n\n")
#     f.close()
# print(removed_count)

    #MAKING THE JSON
    with open("D:\\Thesis\\landslide\\new_multiple_masters\\new_"+index+"_data\\set_archetypes.txt", "r") as f:
        lines=[x for x in f.readlines() if x!="\n"]

        count=0
        for arch in range(0,10):
            masters[arch][ind]=[]
            for line in [x+")" for x in lines[arch][1:-1].split(")")][:-1]:
                count+=1
                new_dict={}
                if line.startswith(", "):
                    line=line[2:]
                split_line=line[1:-4].split("\"")
                if len(split_line)==1:
                    split_line.append("{}")
                    split_line[0]=split_line[0][:-3]

                repr = set([x.strip().replace("'","") for x in split_line[0][1:-3].split(",")])
                new_dict["Representation"]=list(repr)
                dict={}
                if "{}" not in split_line[1]:
                    for i in split_line[1][1:-1].split(","):
                        key=int(i[:i.find(":")].replace("'",""))
                        value=str(i[i.find(":")+1:][2:-1])
                        dict[key]=value

                new_dict["Mapping"]=dict

                masters[arch][ind].append(new_dict)

with open("D://Thesis//landslide//new_multiple_masters//masters.json","w") as fp:
    json.dump(masters,fp)


