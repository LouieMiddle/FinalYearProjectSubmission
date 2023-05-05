from matplotlib import pyplot as plt

from data_processing.query_utils import filter_by_pitch_x_pitch_y, cumulative, load_csv_data_mipl


def plot_all_innings_over_overs(data, axes):
    total_runs = []
    for over in range(1, 21):
        over_data = data[data['delivery_over'] == str(over)]
        over_runs = sum(over_data.runs)
        total_runs.append(over_runs)

    axes.plot(cumulative(total_runs), lw=0.5)


mipl_csv = load_csv_data_mipl()
mipl_csv = filter_by_pitch_x_pitch_y(mipl_csv)
mipl_csv[['delivery_innings', 'delivery_over', 'delivery_ball']] = mipl_csv['delivery'].str.split('.', 3, expand=True)

matches = mipl_csv.groupby('matchId')

i = 0
for matchId, match in matches:
    fig, ax = plt.subplots(1, 2, figsize=(14, 8))

    ax[0].set_xlabel("balls/overs")
    ax[0].set_ylabel("runs")
    ax[1].set_xlabel("balls/overs")
    ax[1].set_ylabel("runs")

    first_innings = match[match['delivery_innings'] == "1"]
    plot_all_innings_over_overs(first_innings, ax[0])

    second_innings = match[match['delivery_innings'] == "2"]
    plot_all_innings_over_overs(second_innings, ax[1])

    plt.show()

    i += 1
