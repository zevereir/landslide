import sys
import os
import comtypes.client
from thesis_sieben_bocklandt.code.prototyping.pdf2ppt import pdf2ppt
from pdf2image import convert_from_path
import pptx
import tkinter
from tkinter import messagebox
from thesis_sieben_bocklandt.code.prototyping.ssim import ssim_compare
def ppt2pdf(file):

    input_file_path = file
    if file.endswith("ppt"):
        output_file_path=file.replace("ppt","pdf")
    elif file.endswith("pptx"):
        output_file_path = file.replace("pptx", "pdf")
    else:
        raise TypeError

    #%% Convert file paths to Windows format
    input_file_path = os.path.abspath(input_file_path)
    output_file_path = os.path.abspath(output_file_path)
    #%% Create powerpoint application object
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    #%% Set visibility to minimize
    powerpoint.Visible = 1
    #%% Open the powerpoint slides
    slides = powerpoint.Presentations.Open(input_file_path)
    #%% Save as PDF (formatType = 32)
    slides.SaveAs(output_file_path, 32)
    #%% Close the slide deck
    slides.Close()
    return output_file_path

def auto_encode(powerpoint, output):

    # pdf = ppt2pdf(powerpoint)
    # pdf2ppt(pdf,output,False,False, True)
    # new_ppt = pptx.Presentation(output+"\\test.pptx")
    # new_ppt.save(output+"\\new_test.pptx")
    # messagebox.showinfo("Title", "Message")
    # new_pdf = ppt2pdf(output+"\\new_test.pptx")
    # os.mkdir(output+"\\new_images")
    # convert_from_path(new_pdf, output_folder=output+"\\new_images", fmt="jpeg", paths_only=True)
    old_dir=output+"\\xml_on_images\\clear_images"
    new_dir=output + "\\new_images"
    old_images=os.listdir(old_dir)
    new_images = os.listdir(new_dir)
    for i in range(0,len(old_images)):
        print(ssim_compare(old_dir+"\\"+old_images[i],new_dir+"\\"+new_images[i], True))
        print("-----")

