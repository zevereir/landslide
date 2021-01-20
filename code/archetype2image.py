import os

from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

#mapping the different xml-tags to the colored boxes
colors={"figure":"b","textbox":"r", "curve":"#ff9500", "rect":"m", "line":"y", "picture":"b","title":"#006600","table":"y","tabletext":"m","caption":"#1eba98","slide_number":"#fcfc00","enlisting":"#108fc2","enlisting_image":"#76c0de","curvetext":"#ba9b1e","normal_text":"r","background":"g","ref":"#8f309c","Mean_Title":"m"}



def archetype2image(output_directory,archetypes, changes):
    """
    Een functie die de juiste titel set boven de extended_image van een slide. De titel is de naam van het archetype    """
    archetypes_names=[(type(x).__name__) for x in archetypes]

    directory = output_directory+"\\xml_on_images"
    arch_directory=directory+"\\archetypal_images"
    if not os.path.isdir(arch_directory):
        os.mkdir(arch_directory)
    for index in range(1,len(archetypes_names)+1):
        showImage_with_archetype(arch_directory+"\\"+str(index)+".png",directory+"\\extended_images\\"+str(index)+".png",archetypes_names[index-1], changes[index-1])


def showImage_with_archetype(filename,path_to_image,archetype, change):
    """
    Effectief de titel erop zetten en de nieuwe afbeelding opslaan.
    """
    im = np.array(Image.open(path_to_image), dtype=np.uint8)
    # Create figure and axes
    fig, ax = plt.subplots(1)
    # Display the image
    ax.imshow(im)
    plt.title(archetype+(change!=[])*" (with changes)")
    plt.savefig(filename)
    plt.close()


