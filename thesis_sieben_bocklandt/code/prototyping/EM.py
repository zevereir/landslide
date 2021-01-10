
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import multivariate_normal
from sklearn.mixture import GaussianMixture
from matplotlib import style

def tenfold_EM(tree):
    means_x = []
    means_y = []
    am_pages=0
    for page in tree.getroot():
        am_pages+=1
        page_size = [float(x) for x in page.attrib.get("bbox").split(",")]
        for element in page.findall("textbox"):
            bbox = [float(x) for x in element.attrib.get("bbox").split(",")]
            mean_x = (bbox[0] + bbox[2]) / (2 * page_size[2])
            mean_y = (bbox[1] + bbox[3]) / (2 * page_size[3])
            if mean_y > 0.5:
                means_x.append(mean_x)
                means_y.append(mean_y)

    if am_pages<2 or len(means_x)<5:
        return None
    GMMS = []
    for i in range(0, 10):
        GMMS.append(EM(means_x, means_y))
    return GMMS


def EM(means_x,means_y):

    # 0. Create dataset
    X=[[x[0],x[1]] for x in list(zip(means_x,means_y))]
    x, y = np.meshgrid(np.sort([v[0] for v in X]), np.sort([v[1] for v in X]))
    XY = np.array([x.flatten(), y.flatten()]).T

    GMM = GaussianMixture(n_components=4).fit(X)  # Instantiate and fit the model
    #print('Converged:', GMM.converged_)  # Check if the model has converged
    #
    # means = GMM.means_
    # covariances = GMM.covariances_
    # # Plot
    # fig = plt.figure(figsize=(10, 10))
    # ax0 = fig.add_subplot(111)
    # ax0.scatter([v[0] for v in X], [v[1] for v in X])
    # for m, c in zip(means, covariances):
    #     multi_normal = multivariate_normal(mean=m, cov=c)
    #     ax0.contour(np.sort([v[0] for v in X]), np.sort([v[1] for v in X]), multi_normal.pdf(XY).reshape(len(X), len(X)), colors='blue',
    #                 alpha=0.3)
    #     ax0.scatter(m[0], m[1], c='grey', zorder=10, s=100)
    # axes = plt.gca()
    # axes.set_xlim([0, 1])
    # axes.set_ylim([0, 1])
    # plt.show()
    # plt.close()
    return GMM
