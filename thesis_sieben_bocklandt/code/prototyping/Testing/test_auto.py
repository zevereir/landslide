from image_similarity_measures.quality_metrics import fsim
import numpy as np
from PIL import Image
from skimage import img_as_float
from pdf2image import convert_from_path
import os
scores=[]
for index in range(2,27):
    print("Slideshow",index)
    data="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\data\\pdf_data_usa\\"+str(index)+".pdf"
    data2="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\data\\pdf_data_usa\\"+str(index)+"_data\\new.pdf"
    os.mkdir("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\data\\pdf_data_usa\\"+str(index)+"_data" + "\\test_images_1")
    os.mkdir("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\data\\pdf_data_usa\\" + str(
        index) + "_data" + "\\test_images_2")
    images_1 = convert_from_path(data, output_folder="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\data\\pdf_data_usa\\"+str(index)+"_data" + "\\test_images_1", fmt="png", paths_only=True)
    images_2 = convert_from_path(data2, output_folder="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\data\\pdf_data_usa\\"+str(index)+"_data" + "\\test_images_2", fmt="png", paths_only=True)
    for i in range(0,len(images_1)):
        print("dia",i+1,len(images_1))
        image1=images_1[i]
        image2=images_2[i]
        im1=Image.open(image1)
        size1=im1.size
        image1 = np.array(im1)
        image2 = np.array(Image.open(image2).resize(size1))
        img1 = img_as_float(image1)
        img2 = img_as_float(image2)
        scores.append(fsim(img1,img2))
print(scores)
print("gemiddelde=",sum(scores)/len(scores))
