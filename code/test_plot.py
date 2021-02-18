from tree2features import tree2features
import xml.etree.ElementTree as ET
for i in range(2,631):
    print(i)
    tree=ET.parse("D://Thesis//landslide//data//Main//"+str(i)+"_data//"+str(i)+"_preparsed.xml")
    xml_file="D://Thesis//landslide//data//Main//"+str(i)+"_data//"+str(i)+".xml"
    output_directory="D://Thesis//landslide//data//Main//"+str(i)+"_data"
    tree2features(tree, xml_file,output_directory, True)