
from thesis_sieben_bocklandt.code.prototyping.data_abstraction import data_abstraction
from datetime import datetime
import xml.etree.ElementTree as ET

from thesis_sieben_bocklandt.code.prototyping.tree2RA import tree2RA
from thesis_sieben_bocklandt.code.prototyping.RA2archetype import RA2archetype
from thesis_sieben_bocklandt.code.prototyping.archetypes2slides import archetypes2slides
from thesis_sieben_bocklandt.code.prototyping.work_with_scores import work_with_scores
from thesis_sieben_bocklandt.code.prototyping.ppt_pdf_similarity import ppt_pdf_similarity
import thesis_sieben_bocklandt.code.prototyping.Testing.test_popc as it

begin=511
end=924
ignore = [1,27,28,36,54,58,64,75,105,112,126,138,154,155,162,185,193,201,203,215,217,223,251,267,272,277,287,292,304,310,311,317,327,332,353,355,362,365,391,408,
 426,442,465,467,487,503,510,532,537,538,551,552,573,599,600,614,618,634,644,653,673,689,696,703,707,734,737,779,786,788,801,810,812,837,839,846,847,868,896,898,901,904,908]
start = datetime.now()
it.init()
numb_iterations=0
for data in range(begin,end):
    print(data)
    if data not in ignore:
        # pdf_file = "D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\" +str(data)+ ".pdf"
        # output_directory = "D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\" +str(data)+ "_data"
        # testing=False
        feature_tree = ET.parse("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\" + str(data) + "_data\\" + str(data) + "_categorized.xml")
        xml_file="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\"+str(data)+"_data\\"+str(data)+".xml"
        output="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\"+str(data)+"_data"
        powerpoint, tree_with_indexes, one_background=tree2RA(feature_tree, xml_file)
        archetypes,changes=RA2archetype(powerpoint)
        used_info = archetypes2slides(archetypes,tree_with_indexes, output, [(page.RA,page.n) for page in powerpoint.pages])
        scores = ppt_pdf_similarity(used_info, xml_file.replace(".xml", "_preparsed.xml"), one_background)
        work_with_scores(scores, archetypes, output)
    #pdf2ppt(pdf_file,output_directory,testing,False)
end=datetime.now()
diff=end-start
print("Total_seconds=",diff.total_seconds())
print("Total_iterations=",it.numb_iterations)
# if begin==1 and end==924:
data_abstraction(1,924,ignore)
