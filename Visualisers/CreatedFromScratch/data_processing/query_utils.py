import os.path

import pandas as pd


def cumulative(lists):
    length = len(lists)
    cu_list = [sum(lists[0:x:1]) for x in range(0, length + 1)]
    return cu_list[1:]


def filter_by_pitch_x_pitch_y(data):
    data = data[(data['pitchX'] >= -2) & (data['pitchX'] <= 2)]
    data = data[(data['pitchY'] >= 0) & (data['pitchY'] <= 14)]
    return data


def load_csv_data_mipl():
    csv_path = os.path.join("../HawkeyeStats-main", "mensIPLHawkeyeStats.csv")
    df = pd.read_csv(csv_path)
    df['pitchX'] = -df['pitchX']
    return df


def load_john_doe():
    csv_path = os.path.join("../pre-processing-csvs", "john_doe_dataset.csv")
    return pd.read_csv(csv_path)


def load_cricket_john_doe():
    def boundary_mapper(run_value):
        if run_value in [0, 1]:
            return 0
        elif run_value in [4, 6]:
            return 1
        else:
            raise ValueError("Invalid batterRuns value")

    john_doe = load_john_doe()

    john_doe = john_doe[
        (john_doe['batterRuns'] == 0) | (john_doe['batterRuns'] == 1) | (john_doe['batterRuns'] == 4) | (
                john_doe['batterRuns'] == 6)]

    john_doe['boundary'] = john_doe['batterRuns'].apply(boundary_mapper)

    return john_doe
