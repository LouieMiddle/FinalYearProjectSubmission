from data_processing.query_utils import load_csv_data_mipl, filter_by_pitch_x_pitch_y

mipl_csv = load_csv_data_mipl()
mipl_csv = filter_by_pitch_x_pitch_y(mipl_csv)

batter_name = "ENTER BATTER NAME"
batter_data = mipl_csv[mipl_csv['batter'] == batter_name]

columns_containing_identifying_information = ['batter', 'batterId', 'nonStriker', 'nonStrikerId', 'bowler', 'bowlerId',
                                              'dismissalDetails', 'matchId']

batter = batter_data.drop(columns=columns_containing_identifying_information)

batter.to_csv('../Pre-processing-csvs/john_doe_dataset.csv')

print("Finished")
