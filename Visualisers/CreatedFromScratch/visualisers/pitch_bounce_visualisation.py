import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

from data_processing.query_utils import load_cricket_john_doe


def set_axes_meta(axes, hand, r):
    axes.set_xlabel("PitchX")
    axes.set_ylabel("PitchY")
    axes.set_title(hand + ", Boundary Scored: " + str(r))


def plot_pitch(axes):
    WICKET_LENGTH = 22.56
    WICKET_WIDTH = 3.66

    BATTING_CREASE_LENGTH = 1.22

    # Draw a pitch surface
    x = [WICKET_WIDTH / 2,
         -WICKET_WIDTH / 2,
         -WICKET_WIDTH / 2,
         WICKET_WIDTH / 2]
    y = [WICKET_LENGTH - BATTING_CREASE_LENGTH,
         WICKET_LENGTH - BATTING_CREASE_LENGTH,
         -BATTING_CREASE_LENGTH,
         -BATTING_CREASE_LENGTH]

    axes.fill(x, y, color='slategray', alpha=0.2)


def plot_deliveries(data, r, hand, axes):
    set_axes_meta(axes, hand, r)
    axes.plot(data[:, 0], data[:, 1], 'k.', markersize=1)
    axes.set_aspect(0.2)
    plot_pitch(axes)


def plot_heatmap(data, r, hand, axes):
    x_min = min(data[:, 0])
    x_max = max(data[:, 0])
    y_min = min(data[:, 1])
    y_max = max(data[:, 1])

    X, Y = np.mgrid[x_min:x_max:100j, y_min:y_max:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([data[:, 0], data[:, 1]])
    kernel = gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    set_axes_meta(axes, hand, r)
    axes.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[x_min, x_max, y_min, y_max])
    axes.set_aspect(0.2)

    plot_pitch(axes)


john_doe = load_cricket_john_doe()

seam = ['FAST_SEAM', 'MEDIUM_SEAM', 'SEAM']
john_doe = john_doe[john_doe['bowlingStyle'].isin(seam)]

fig, ax = plt.subplots(2, 4, figsize=(18, 10))

boundaries = john_doe.boundary.unique()

for i, boundary in enumerate(boundaries):
    data = john_doe[john_doe['boundary'] == boundary]

    rh = data[data.rightArmedBowl == True]
    xy = np.array(rh[['pitchX', 'pitchY']])
    plot_deliveries(xy, boundary, "Right Arm Delivery", ax[i, 0])
    plot_heatmap(xy, boundary, "Right Arm Delivery", ax[i, 1])

    lh = data[data.rightArmedBowl == False]
    xy = np.array(lh[['pitchX', 'pitchY']])
    plot_deliveries(xy, boundary, "Left Arm Delivery", ax[i, 2])
    plot_heatmap(xy, boundary, "Left Arm Delivery", ax[i, 3])

plt.show()
fig.savefig('../figures/pitch_bounce.png')
