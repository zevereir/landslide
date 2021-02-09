import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

for i in range(43,841):
    print(i)
    images=[mpimg.imread("D://Thesis//landslide//data//american//pdf_images//"+str(i)+"_data//"+z) for z in os.listdir("D://Thesis//landslide//data//american//pdf_images//"+str(i)+"_data")[0:4]]
    if len(images)==2:

        fig, axs = plt.subplots(2, figsize=(15,12))

        axs[0].imshow(images[0])
        axs[1].imshow(images[1])
        axs[0].axis("off")
        axs[1].axis("off")
    elif len(images)==3:

        fig, axs = plt.subplots(2, 2, figsize=(15,12))
        axs[0,0].imshow(images[0])
        axs[0,1].imshow(images[1])
        axs[1,0].imshow(images[2])

        axs[0,0].axis("off")
        axs[0,1].axis("off")
        axs[1,0].axis("off")
    else:

        fig, axs = plt.subplots(2, 2, figsize=(15,12))
        axs[0,0].imshow(images[0])
        axs[0,1].imshow(images[1])
        axs[1,0].imshow(images[2])
        axs[1,1].imshow(images[3])
        axs[0,0].axis("off")
        axs[0,1].axis("off")
        axs[1,0].axis("off")
        axs[1,1].axis("off")

    plt.savefig("D://Thesis//landslide//data//slideshow_images//"+str(i)+".png")
    plt.close()