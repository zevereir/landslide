import os

from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

#mapping the different xml-tags to the colored boxes
colors={"figure":"b","textbox":"r", "curve":"#ff9500", "rect":"m", "line":"y", "picture":"b","title":"#006600","table":"y","tabletext":"m","caption":"#1eba98","slide_number":"#fcfc00","enlisting":"#108fc2","enlisting_image":"#76c0de","curvetext":"#ba9b1e","normal_text":"r","background":"g","ref":"#8f309c","Mean_Title":"m", "combined_pictures":"b"}



def xml2image(pdf_file, xml_tree, output_directory, add_text):
    directory = output_directory+"\\xml_on_images"
    if not os.path.isdir(directory):
        os.mkdir(directory)
        os.mkdir(directory+"\\clear_images")

    print("Pdf omzetten naar foto's")
    if pdf_file!="":
        images=convert_from_path(pdf_file, output_folder=directory+"\\clear_images", fmt="jpeg", paths_only=True)
    else:
        if not os.path.isdir(directory+"\\extended_images"):
            os.mkdir(directory+"\\extended_images")
        images=os.listdir(directory+"\\clear_images")
    amount = len(images)+1
    print("XML parsen")
    root = xml_tree.getroot()
    rectangles_per_page=[]
    for page in root:
        attributes = page.attrib
        size = attributes.get("bbox").split(",")
        rectangles = [(float(size[2]), float(size[3]))]
        mean_title=attributes.get("mean_title")
        if mean_title!= None:
            bbox=[float(x) for x in mean_title.strip('][').split(', ')]
            x1 = bbox[0]
            y1 = bbox[1]
            x2 = bbox[2]
            y2 = bbox[3]
            length = abs(x2 - x1)
            width = abs(y2 - y1)
            rectangles.append([x1, y2, length, width, colors.get("Mean_Title"), "Mean_Title"])
        # print(size)
        for child in page:
            if child.tag in colors.keys():
                child_attributes = child.attrib
                if len(child_attributes)!=0:
                    child_size = child_attributes.get("bbox").split(",")
                    x1 = float(child_size[0])
                    y1 = float(child_size[1])
                    x2 = float(child_size[2])
                    y2 = float(child_size[3])
                    length = abs(x2 - x1)
                    width = abs(y2 - y1)
                    rectangles.append([x1, y2, length, width,colors.get(child.tag),child.tag])
        rectangles_per_page.append(rectangles)

    print("Images maken")
    extra=""
    if pdf_file=="":
        extra=directory+"\\clear_images\\"


    for page_id in range(1,amount):
        if pdf_file=="":
            filename = directory + "\\extended_images\\" + str(page_id) + ".png"
        else:
            filename=directory+"\\"+str(page_id)+".png"
        showImage_with_rectangles(filename,extra+images[page_id-1],rectangles_per_page[page_id-1], add_text)


def showImage_with_rectangles(filename,path_to_image,rectangles, add_text):
    im = np.array(Image.open(path_to_image), dtype=np.uint8)
    shape=im.shape
    xml_shape=rectangles.pop(0)
    x=shape[1]
    y=shape[0]
    xml_x=xml_shape[0]
    xml_y=xml_shape[1]
    x_factor=x/xml_x
    y_factor=y/xml_y
    # Create figure and axes
    fig, ax = plt.subplots(1)
    # Display the image
    ax.imshow(im)
    for rectangle in rectangles:
        # Create a Rectangle patch (xy) upper left, width, height
        upper_left_x=rectangle[0]*x_factor
        upper_left_y=y-rectangle[1]*y_factor
        length=rectangle[2]*x_factor
        width=rectangle[3]*y_factor
        rect = patches.Rectangle((upper_left_x,upper_left_y), length,width, linewidth=1, edgecolor=rectangle[4], facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
        if add_text:
            plt.text(upper_left_x,upper_left_y,rectangle[5],bbox=dict(facecolor='white', alpha=0.5))
    plt.savefig(filename)
    plt.close()


