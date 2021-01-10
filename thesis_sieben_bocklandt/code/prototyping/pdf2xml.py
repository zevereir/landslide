import os
import shutil
def pdf2xml(pdf_file, output_directory):
    """
    Een functie die via pdf2text.py een pdf omzet naar een xml-file met daarin de tekst, images en hun coordinaten
    :param pdf_file: het pad van de pdf_file
    :param output_directory: een directory waar alle foto's en de xml komen
    :return:
    """
    if pdf_file.find("\\")==-1:
        filename = "/"+pdf_file.split("/")[-1].replace(".pdf",".xml")
    else:
        filename = "\\"+pdf_file.split("\\")[-1].replace(".pdf", ".xml")
    output_file=output_directory+filename
    output_images=output_directory+"\\images"

    while os.path.isdir(output_directory):
        try:
            shutil.rmtree(output_directory)
        except:
            pass
    while not os.path.isdir(output_directory):
        try:
            os.mkdir(output_directory)
        except:
            pass
    os.mkdir(output_directory+"\\images")
    open(output_file, 'a').close()
    os.system("python D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\code\\prototyping\\pdf2txt.py -t xml -O "+output_images+" -o "+output_file+" -A "+pdf_file)
    return output_file