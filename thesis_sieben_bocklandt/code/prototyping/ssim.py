
import matplotlib.pyplot as plt
from skimage import data, img_as_float
from skimage.metrics import structural_similarity as ssim_ori
from skimage.metrics import mean_squared_error
from scipy.stats import wasserstein_distance
from imageio import imread
from skimage.transform import resize
from skimage.measure import compare_ssim
import imagehash
import numpy as np
from PIL import Image
from image_similarity_measures.quality_metrics import fsim
from thesis_sieben_bocklandt.code.prototyping.timing import calc_signature_similarity
from thesis_sieben_bocklandt.code.prototyping.dtw import ddtw

def phash(img1,img2):

    hash = imagehash.phash(Image.open(img1),32)
    otherhash = imagehash.phash(Image.open(img2),32)
    return hash - otherhash

def earth_movers_distance(path_a, path_b):
  '''
  Measure the Earth Mover's distance between two images
  @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
  @returns:
    TODO
  '''
  img_a = get_img(path_a, norm_exposure=True)
  img_b = get_img(path_b, norm_exposure=True)
  hist_a = get_histogram(img_a)
  hist_b = get_histogram(img_b)
  return wasserstein_distance(hist_a, hist_b)

def get_img(path, norm_size=True, norm_exposure=False):
  '''
  Prepare an image for image processing tasks
  '''
  # specify resized image sizes
  height = 2 ** 10
  width = 2 ** 10
  # flatten returns a 2d grayscale array
  img = imread(path, as_gray=True).astype(int)
  # resizing returns float vals 0:255; convert to ints for downstream tasks
  if norm_size:
    img = resize(img, (height, width), anti_aliasing=True, preserve_range=True)
  if norm_exposure:
    img = normalize_exposure(img)
  return img
def normalize_exposure(img):
  '''
  Normalize the exposure of an image.
  '''
  img = img.astype(int)
  hist = get_histogram(img)
  # get the sum of vals accumulated by each position in hist
  cdf = np.array([sum(hist[:i+1]) for i in range(len(hist))])
  # determine the normalization values for each unit of the cdf
  sk = np.uint8(255 * cdf)
  # normalize each position in the output image
  height, width = img.shape
  normalized = np.zeros_like(img)
  for i in range(0, height):
    for j in range(0, width):
      normalized[i, j] = sk[img[i, j]]
  return normalized.astype(int)
def get_histogram(img):
  '''
  Get the histogram of an image. For an 8-bit, grayscale image, the
  histogram will be a 256 unit vector in which the nth value indicates
  the percent of the pixels in the image with the given darkness level.
  The histogram's values sum to 1.
  '''
  h, w = img.shape
  hist = [0.0] * 256
  for i in range(h):
    for j in range(w):
      hist[img[i, j]] += 1
  return np.array(hist) / (h * w)

from PIL import ImageChops
import math, operator
import functools
def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(functools.reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1]))

def structural_sim(path_a, path_b):
  '''
  Measure the structural similarity between two images
  @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
  @returns:
    {float} a float {-1:1} that measures structural similarity
      between the input images
  '''
  img_a = get_img(path_a)
  img_b = get_img(path_b)
  sim, diff = compare_ssim(img_a, img_b, full=True)
  return sim

import timeit
def time_functions(image1,image2):
    times=10
    global test
    test=image1
    global test2
    test2=image2
    time_mse=timeit.timeit('image1=np.array(Image.open(test));image2 = np.array(Image.open(test2));img1 = img_as_float(image1);img2 = img_as_float(image2);mse_none = mean_squared_error(img1, img2);',number=times,setup='import numpy as np;from PIL import Image',globals=globals())/times
    time_ssim = timeit.timeit('image1=np.array(Image.open(test));image2 = np.array(Image.open(test2));img1 = img_as_float(image1);img2 = img_as_float(image2);ssim_new = ssim_ori(img1, img2,multichannel=True)', number=times,setup='import numpy as np;from PIL import Image',globals=globals()) / times
    time_sign=timeit.timeit('calc_signature_similarity(test,test2);',number=times, setup="from thesis_sieben_bocklandt.code.prototyping.timing import calc_signature_similarity", globals=globals())/times
    return time_mse,time_ssim,time_sign


def ssim_compare(image1,image2, visualize):
    signature_simil = calc_signature_similarity(image1,image2)
    signature_0=calc_signature_similarity(image1,image1)
    dtw_img1 =Image.open(image1)
    dtw_img2 = Image.open(image2)
    x,y=dtw_img1.size
    factor=120
    dtw_img1_new=np.mean(np.array(dtw_img1.resize((int(x/factor),int(y/factor)))),axis=2)
    dtw_img2_new = np.mean(np.array(dtw_img2.resize((int(x/factor), int(y/factor)))),axis=2)


    image1=np.array(Image.open(image1))
    image2 = np.array(Image.open(image2))




    img1 = img_as_float(image1)
    img2 = img_as_float(image2)
    fsimm = fsim(img1,img2)
    #dtw = ddtw(dtw_img1_new, dtw_img2_new)
    mse_new = mean_squared_error(img1, img2)
    ssim_new = ssim_ori(img1, img2,multichannel=True)


    if visualize:
        mse_none = mean_squared_error(img1, img1)
        ssim_none = ssim_ori(img1, img1, data_range=img1.max() - img1.min(), multichannel=True)

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4),
                                 sharex=True, sharey=True)
        ax = axes.ravel()
        label = 'MSE: {:.4f}, SSIM: {:.4f}, LSH: {:.4f}'

        ax[0].imshow(img1, cmap=plt.cm.gray, vmin=0, vmax=1)
        ax[0].set_xlabel(label.format(mse_none, ssim_none,signature_0))
        ax[0].set_title('Originele dia')

        ax[1].imshow(img2, cmap=plt.cm.gray, vmin=0, vmax=1)
        ax[1].set_xlabel(label.format(mse_new, ssim_new, signature_simil))
        ax[1].set_title('Gereconstrueerde dia')
        plt.tight_layout()
        plt.show()
    return (1-mse_new, ssim_new, signature_simil,fsimm,(fsimm+(ssim_new+signature_simil)/2)/2)