import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

from data_processing.query_utils import load_cricket_john_doe


def plot_heatmap(data, r, axes):
    x_min = min(data[:, 0])
    x_max = max(data[:, 0])
    y_min = min(data[:, 1])
    y_max = max(data[:, 1])

    X, Y = np.mgrid[x_min:x_max:100j, y_min:y_max:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([data[:, 0], data[:, 1]])
    kernel = gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    axes.set_title("Left Arm Delivery, Boundary Scored: " + str(r))
    axes.set_xlabel("StumpsX")
    axes.set_ylabel("StumpsY")
    axes.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[x_min, x_max, y_min, y_max])
    axes.plot(data[:, 0], data[:, 1], 'k.', markersize=1)

    STUMP_HEIGHT = 0.7112
    STUMP_GAP = 0.08893

    axes.set_ylim(-0.5, 2.5)
    axes.set_xlim(-2, 2)

    # Draw stumps
    x = [0, 0]
    y = [0, STUMP_HEIGHT]
    axes.plot(x, y, color='darkviolet', linewidth=3, zorder=10)

    x = [STUMP_GAP, STUMP_GAP]
    y = [0, STUMP_HEIGHT]
    axes.plot(x, y, color='darkviolet', linewidth=3, zorder=10)

    x = [-STUMP_GAP, -STUMP_GAP]
    y = [0, STUMP_HEIGHT]
    axes.plot(x, y, color='darkviolet', linewidth=3, zorder=10)


john_doe = load_cricket_john_doe()

seam = ['FAST_SEAM', 'MEDIUM_SEAM', 'SEAM']
john_doe = john_doe[john_doe['bowlingStyle'].isin(seam)]
john_doe = john_doe[john_doe['rightArmedBowl'] == False]

fig, ax = plt.subplots(1, 2, figsize=(10, 6))

boundaries = john_doe.boundary.unique()

for i, boundary in enumerate(boundaries):
    data = john_doe[john_doe['boundary'] == boundary]

    xy = np.array(data[['stumpsX', 'stumpsY']])
    plot_heatmap(xy, boundary, ax[i])

plt.show()
fig.savefig('../figures/post_wicket_left_arm.png')
