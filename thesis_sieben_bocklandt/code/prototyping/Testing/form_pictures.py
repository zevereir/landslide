from matplotlib import pyplot as plt
from skimage import img_as_float
import numpy as np
from PIL import Image

data="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\User study\\"
image1=data+"11.png"
image2=data+"12.png"
image3=data+"14.png"

img1 = img_as_float(np.array(Image.open(image1)))
img2 = img_as_float(np.array(Image.open(image2)))
img3 = img_as_float(np.array(Image.open(image3)))
import numpy as np
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
from pylab import *
# Create 2x2 sub plots
gs = gridspec.GridSpec(2, 2)

pl.figure(figsize=[10,10])

ax = pl.subplot(gs[0, :]) # row 0, col 0
ax.imshow(img1, cmap=plt.cm.gray, vmin=0, vmax=1)
ax.set_title('Originele dia')
ax.axis('off')
autoAxis = ax.axis()
rec = Rectangle((autoAxis[0]-0.7,autoAxis[2]-0.2),(autoAxis[1]-autoAxis[0])+1,(autoAxis[3]-autoAxis[2])+0.4,fill=False,lw=2)
rec = ax.add_patch(rec)
rec.set_clip_on(False)
ax = pl.subplot(gs[1, 0]) # row 0, col 1
pl.plot([0,1])
ax.imshow(img2, cmap=plt.cm.gray, vmin=0, vmax=1)
ax.set_title('A')
ax.axis('off')
autoAxis = ax.axis()
rec = Rectangle((autoAxis[0]-0.7,autoAxis[2]-0.2),(autoAxis[1]-autoAxis[0])+1,(autoAxis[3]-autoAxis[2])+0.4,fill=False,lw=2)
rec = ax.add_patch(rec)
rec.set_clip_on(False)
ax = pl.subplot(gs[1, 1]) # row 1, span all columns
pl.plot([0,1])
ax.imshow(img3, cmap=plt.cm.gray, vmin=0, vmax=1)
ax.set_title('B')
ax.axis('off')
autoAxis = ax.axis()
rec = Rectangle((autoAxis[0]-0.7,autoAxis[2]-0.2),(autoAxis[1]-autoAxis[0])+1,(autoAxis[3]-autoAxis[2])+0.4,fill=False,lw=2)
rec = ax.add_patch(rec)
rec.set_clip_on(False)
# ax[0].imshow(img1, cmap=plt.cm.gray, vmin=0, vmax=1)
# ax[0].set_title('Originele dia')

# ax[1].imshow(img2, cmap=plt.cm.gray, vmin=0, vmax=1)
# ax[1].set_title('A')

plt.show()
plt.close()