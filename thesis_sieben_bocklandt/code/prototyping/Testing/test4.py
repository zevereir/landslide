from thesis_sieben_bocklandt.code.prototyping.tree2features import tree2features
from thesis_sieben_bocklandt.code.prototyping.pdf2xml import pdf2xml
from thesis_sieben_bocklandt.code.prototyping.xml2image import xml2image
from thesis_sieben_bocklandt.code.prototyping.xml_preparse2tree import preparse_xml
from thesis_sieben_bocklandt.code.prototyping.tree2features import tree2features
from thesis_sieben_bocklandt.code.prototyping.tree2RA import tree2RA
from thesis_sieben_bocklandt.code.prototyping.RA2archetype import RA2archetype
from thesis_sieben_bocklandt.code.prototyping.archetypes2slides import archetypes2slides
from thesis_sieben_bocklandt.code.prototyping.clustering import k_modes
import xml.etree.ElementTree as ET

# pdf="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\test\\RA.pdf"
# xml_file=pdf2xml(pdf,output)
# xml_tree = preparse_xml(xml_file,output)
# feature_tree = tree2features(xml_tree, xml_file,output, True)
# for data in range(2,9):
#     print(data)
#     feature_tree=ET.parse("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\"+str(data)+"_data\\"+str(data)+"_categorized.xml")
#     xml_file="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\"+str(data)+"_data\\"+str(data)+".xml"
#     output="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\"+str(data)+"_data"
#     powerpoint, tree_with_indexes, one_background=tree2RA(feature_tree, xml_file)
#     archetypes,changes=RA2archetype(powerpoint)
#     archetypes2slides(archetypes,tree_with_indexes, output, [(page.RA,page.n) for page in powerpoint.pages])



# data=[]
# for ppt in powerpoint.pages:
#     data.append((ppt.RA,ppt.n))
# k=8
# clusters,centroids = k_modes(k,data)
# print("------------------------")
# for i in range(0,k):
#     print(len(clusters[i]),centroids[i])


#
import ast
print("start_data")
f=open("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\clustering\\clusters.txt",'r')
data=[ast.literal_eval(next(f)) for x in range(80)]
f.close()
print("data_done")
k = 20
clusters,centroids = k_modes(k,data)
print("------------------------")
for i in range(0,k):
    print(len(clusters[i]),centroids[i])