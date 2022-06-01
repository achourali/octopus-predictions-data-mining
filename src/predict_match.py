from datetime import datetime
import pickle
import pandas as pd


def predict_match(leagueId, homeTeam, awayTeam, date):

    with open(f'src/models/{leagueId}.params.pkl', 'rb') as handle:
        params = pickle.load(handle)
    classifiers = pd.read_pickle(f'src/models/{leagueId}.classifiers.pkl')

    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').toordinal()
    match_row = []

    # normalising date
    date = (date-params['scaler_data_min_']) / \
        (params['scaler_data_max_']-params['scaler_data_min_'])

    for column in params['data_columns']:
        if(column == 'date'):
            match_row.append(date)
        elif(column == f'homeTeam_{homeTeam}'):
            match_row.append(1)
        elif(column == f'awayTeam_{awayTeam}'):
            match_row.append(1)
        else:
            match_row.append(0)

    data_to_predict = pd.DataFrame([match_row], columns=params['data_columns'])

    predictions = []

    for index, classifier in classifiers.iterrows():
        prediction = []
        for target_label in params['targets_keys']:
            prediction.append(
                classifier[target_label].predict(data_to_predict)[0])
        predictions.append(prediction)

    predictions = pd.DataFrame(predictions, columns=params['targets_keys'])


    response = {}

    for target_label in params['targets_keys']:
        most_common_value = predictions.loc[:, target_label].value_counts().index.tolist()[
            0]

        if(target_label == 'result'):
            percent = predictions.loc[:, target_label].value_counts(
            )[most_common_value]/predictions.loc[:, target_label].count()

            if(percent == 1):
                percent = 0.9
            response[target_label] = {most_common_value: percent}
        else:

            if(most_common_value != 1):
                percent = 0.1
            else:
                percent = predictions.loc[:, target_label].value_counts(
                )[most_common_value]/predictions.loc[:, target_label].count()

            if(percent == 1):
                percent = 0.9

            response[target_label] = percent

