# from pptx import Presentation
# from pptx.shapes.placeholder import PicturePlaceholder, BasePlaceholder, TablePlaceholder
# import itertools
# from pptx.util import Pt
# from PIL import Image
# #
# # TITLE_SLIDE = 0
# # SINGLE_CONTENT = 1
# # DOUBLE_CONTENT = 2
# # TRIPLE_CONTENT = 3
# # COMPARISON =4
# # SECTION_HEADER = 5
# # TITLE_ONLY = 6
# # CAPTIONED_CONTENT = 7
# # BACKGROUND_QUOTE = 8
# # BACKGROUND_ONLY = 9
# # CONTENT_ONLY = 10
# #
# #
# # def add_image(slide, placeholder, source, background):
# #     """"
# #     functie om een afbeelding toe te voegen aan een al bestaande placeholder
# #     """
# #     single_content = PicturePlaceholder(placeholder._sp, slide)
# #     width, height = Image.open(source).size
# #     # Make sure the placeholder doesn't zoom in
# #     single_content.height = height
# #     single_content.width = width
# #     single_content = single_content.insert_picture(source)
# #     # Calculate ratios and compare
# #     if not background:
# #         image_ratio = width / height
# #         placeholder_ratio = single_content.width / single_content.height
# #         ratio_difference = placeholder_ratio - image_ratio
# #         # Placeholder width too wide:
# #         if ratio_difference > 0:
# #             difference_on_each_side = ratio_difference / 2
# #             single_content.crop_left = -difference_on_each_side
# #             single_content.crop_right = -difference_on_each_side
# #         # Placeholder height too high
# #         else:
# #             difference_on_each_side = -ratio_difference / 2
# #             single_content.crop_bottom = -difference_on_each_side
# #             single_content.crop_top = -difference_on_each_side
# #     width = single_content.width
# #     height = single_content.height
# #     left = single_content.left
# #     top = single_content.top + height
# #
# # def get_combinations(layout):
# #     amount_of_placeholders=[2,2,3,4,5,2,1,3,2,1]
# #     combinations=[]
# #     if layout != 7 or layout !=9:
# #         combinations.append([0,1])
# #     while len(combinations)<amount_of_placeholders[layout]:
# #         combinations.append([0,1,2])
# #     if layout in [8,9]:
# #         combinations[-1]=[-1]
# #     return set(itertools.product(*combinations))
# #
# #
# #
# # def remove_slides(begin,end, pres):
# #     for i in range(end, begin-1, -1):
# #         rId = pres.slides._sldIdLst[i].rId
# #         pres.part.drop_rel(rId)
# #         del pres.slides._sldIdLst[i]
# #
# #
# #
# # dummy=["Lorem","Lorem ipsum dolor sit amet","Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."]
# # path1=("D://Thesis//landslide//testdia1.pptx")
# # mapping=[[0,1],[0,1],[0,1,2],[0,1,13,14],[0,1,3,2,4],[0,1],[0],[0,1,2],[0,13],[13]]
# # front_sign=["A","B","C","D","E"]
# # for master in range(0,1):
# #     print("MASTER",master)
# #     if master==0:
# #         lay_map=[x for x in range(0,10)]
# #     else:
# #         lay_map=[0,1,3,13,4,2,5,8,14,15]
# #     prs=Presentation("D://Thesis//landslide//new_multiple_masters//"+str(master)+".pptx")
# #     for layout in range(0,10):
# #         map=mapping[layout]
# #         for combo in get_combinations(layout):
# #             slide=prs.slides.add_slide(prs.slide_layouts[lay_map[layout]])
# #             for v in slide.placeholders:
# #                 print(v.placeholder_format.idx, v.placeholder_format.type)
# #             for i in range(0,len(map)):
# #                 if combo[i]>=0:
# #                     placeholder=slide.placeholders[map[i]]
# #                     tf = placeholder.text_frame
# #                     tf.text = front_sign[i]+dummy[combo[i]]
# #                     if layout==7 or map[i]!=0:
# #                         for para in tf.paragraphs:
# #                             para.font.size = Pt(20)
# #                 else:
# #                     add_image(slide,slide.placeholders[map[i]],"D://Thesis//landslide//marimba.jpg",True)
# #     prs.save("D://Thesis//landslide//new_multiple_masters//new_"+str(master)+".pptx")
# #
# # #
# #
#
# # %% Convert a Folder of PowerPoint PPTs to PDFs
#
# # Purpose: Converts all PowerPoint PPTs in a folder to Adobe PDF
#
# # Author:  Matthew Renze
#
# # Usage:   python.exe ConvertAll.py input-folder output-folder
# #   - input-folder = the folder containing the PowerPoint files to be converted
# #   - output-folder = the folder where the Adobe PDFs will be created
#
# # Example: python.exe ConvertAll.py C:\InputFolder C:\OutputFolder
#
# # Note: Also works with PPTX file format
#
# # %% Import libraries
# import sys
# import os
# import comtypes.client
# import os
# import sys
# import comtypes.client
#
#
# def ppt_2_pdf(input_ppt_file, output_pdf_file, format_type=32):
#     """
#     Convert a Powerpoint file to a pdf file
#     :param input_ppt_file: input Powerpoint file
#     :param output_pdf_file: output pdf file
#     :param format_type:
#     :return: a pdf file written in the directory
#     """
#     powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
#     powerpoint.Visible = 1
#
#     if output_pdf_file[-3:] != 'pdf':
#         output_pdf_file = output_pdf_file + ".pdf"
#
#     ppt_file = powerpoint.Presentations.Open(input_ppt_file)
#     ppt_file.SaveAs(output_pdf_file, format_type)
#     ppt_file.Close()
#     powerpoint.Quit()
#
#
# def convert_all_ppt(directory):
#     """
#     Convert all Powerpoint files in the same directory to pdf files
#     :param directory: the full path to the directory
#     :return: all pdf outputs in the same directory
#     """
#     try:
#         for file in os.listdir(directory):
#             _, file_extension = os.path.splitext(file)
#             if "ppt" in file_extension:
#                 input_file = directory + "\\" + file
#                 output_file = input_file + "_output.pdf"
#                 ppt_2_pdf(input_file, output_file)
#     except FileNotFoundError:
#         print("The system cannot file directory \'{0}\'".format(directory))
#         exit(2)
#     except OSError:
#         print("The filename, directory name, or volume label syntax is incorrect: \'{0}\'"
#               .format(directory))
#         exit(2)
#
#
# # %% Convert each file
# for i in range(23,35):
# # %% Get console arguments
#     input_folder_path = "D:\\Thesis\\landslide\\new_multiple_masters\\new_"+str(i)+".pptx"
#     output_folder_path = "D:\\Thesis\\landslide\\new_multiple_masters\\new_"+str(i)+".pdf"
#
#
#     # %% Convert folder paths to Windows format
#     input_folder_path = os.path.abspath(input_folder_path)
#     output_folder_path = os.path.abspath(output_folder_path)
#
#
#     ppt_2_pdf(input_folder_path,output_folder_path)
#     # Skip if file does not contain a power point extension
#
#
#
# """
#     A simple Python script to convert all Powerpoint files in a certain directory to
#     pdf files in Windows environment.
#     Usage: python ppt2pdf.py -p <path_to_source_directory>
#     Dependency:
#         The script uses comtypes. Install it by 'pip install comtypes'
# """
# import os
# import sys
# import comtypes.client
#
#
# def ppt_2_pdf(input_ppt_file, output_pdf_file, format_type=32):
#     """
#     Convert a Powerpoint file to a pdf file
#     :param input_ppt_file: input Powerpoint file
#     :param output_pdf_file: output pdf file
#     :param format_type:
#     :return: a pdf file written in the directory
#     """
#     powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
#     powerpoint.Visible = 1
#
#     if output_pdf_file[-3:] != 'pdf':
#         output_pdf_file = output_pdf_file + ".pdf"
#
#     ppt_file = powerpoint.Presentations.Open(input_ppt_file)
#     ppt_file.SaveAs(output_pdf_file, format_type)
#     ppt_file.Close()
#     powerpoint.Quit()
#
#
# def convert_all_ppt(directory):
#     """
#     Convert all Powerpoint files in the same directory to pdf files
#     :param directory: the full path to the directory
#     :return: all pdf outputs in the same directory
#     """
#     try:
#         for file in os.listdir(directory):
#             _, file_extension = os.path.splitext(file)
#             if "ppt" in file_extension:
#                 input_file = directory + "\\" + file
#                 output_file = input_file + "_output.pdf"
#                 ppt_2_pdf(input_file, output_file)
#     except FileNotFoundError:
#         print("The system cannot file directory \'{0}\'".format(directory))
#         exit(2)
#     except OSError:
#         print("The filename, directory name, or volume label syntax is incorrect: \'{0}\'"
#               .format(directory))
#         exit(2)
#
#
import shutil
import os

from pathlib import Path
Path("D:\\User\\Documents\\School\\SandSlide_data\\Main").mkdir(parents=True, exist_ok=True)
for i in range(500,631):
    Path("D:\\User\\Documents\\School\\SandSlide_data\\Main\\"+str(i)+"_data").mkdir(parents=True, exist_ok=True)
    for it in os.listdir(Path("D://Thesis//landslide//data//Main//"+str(i)+"_data")):
        if not it.endswith(".png") and "images" not in it:

            shutil.copyfile(Path("D://Thesis//landslide//data//Main//"+str(i)+"_data//"+it),Path("D:\\User\\Documents\\School\\SandSlide_data\\Main\\"+str(i)+"_data\\"+it))
    Path("D:\\User\\Documents\\School\\SandSlide_data\\Main\\"+str(i)+"_data\\"+"images").mkdir(parents=True, exist_ok=True)
    for pic in os.listdir("D://Thesis//landslide//data//Main//"+str(i)+"_data//images"):
        shutil.copyfile(Path("D://Thesis//landslide//data//Main//"+str(i)+"_data//images//"+pic),Path("D:\\User\\Documents\\School\\SandSlide_data\\Main\\"+str(i)+"_data\\"+"images\\"+pic))