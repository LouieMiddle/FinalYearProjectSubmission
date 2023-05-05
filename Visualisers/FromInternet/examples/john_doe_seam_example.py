import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plots.pitch_heatmap import pitch_heatmap


df = pd.read_csv('../data/john_doe_dataset.csv')

seam = ['FAST_SEAM', 'MEDIUM_SEAM', 'SEAM']
df = df[df['bowlingStyle'].isin(seam)]
df = df[df['rightArmedBowl'] == True]

xy = np.array(df[['pitchX', 'pitchY']])
runs = df.batterRuns

title = 'A Batter'
subtitle_1 = 'All IPL deliveries against right arm seam for a single batter'
subtitle_2 = 'From {0} balls faced with tracking enabled'.format(len(xy))
legend_title = 'Strike Rate'

pitch_heatmap(xy, runs, title, subtitle_1, subtitle_2, legend_title, min_balls=6, show_markers=True,
              measure='strike_rate')

plt.show()
