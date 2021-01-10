import os
from shutil import copyfile
ignore = [1,27,28,36,54,58,64,75,105,112,126,138,154,155,162,185,193,201,203,215,217,223,251,267,272,277,287,292,304,310,311,317,327,332,353,355,362,365,391,408,
 426,442,465,467,487,503,510,532,537,538,551,552,573,599,600,614,618,634,644,653,673,689,696,703,707,734,737,779,786,788,801,810,812,837,839,846,847,868,896,898,901,904,908]
count=1
for i in range(1,924):
    if i not in ignore:
        # try:
        #     os.mkdir("D:\\Thesis\\landslide_data\\"+str(count)+"_data")
        # except:
        #     pass
        # try:
        #     os.mkdir("D:\\Thesis\\landslide_data\\"+str(count)+"_data\\results")
        # except:
        #     pass
        try:
            copyfile("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\"+str(i)+"_data\\"+str(i)+"_preparsed.xml","D:\\Thesis\\landslide_data\\"+str(count)+"_data\\"+str(count)+"_preparsed.xml")
        except:
            pass
        count+=1
