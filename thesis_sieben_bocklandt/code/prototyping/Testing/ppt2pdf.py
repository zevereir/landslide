
# %% Convert a Folder of PowerPoint PPTs to PDFs

# Purpose: Converts all PowerPoint PPTs in a folder to Adobe PDF

# Author:  Matthew Renze

# Usage:   python.exe ConvertAll.py input-folder output-folder
#   - input-folder = the folder containing the PowerPoint files to be converted
#   - output-folder = the folder where the Adobe PDFs will be created

# Example: python.exe ConvertAll.py C:\InputFolder C:\OutputFolder

# Note: Also works with PPTX file format

# %% Import libraries
import sys
import os
import comtypes.client

# %% Get console arguments
input_folder_path = "D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\ppt_data_usa"
output_folder_path = "D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa"

# %% Convert folder paths to Windows format
input_folder_path = os.path.abspath(input_folder_path)
output_folder_path = os.path.abspath(output_folder_path)

# %% Get files in input folder
input_file_paths = os.listdir(input_folder_path)
counter=1
# %% Convert each file
for i in range(0,100):
    input_file_name=input_file_paths[i]
    print(input_file_name)
    x=input("ga verder")
     # Skip if file does not contain a power point extension




