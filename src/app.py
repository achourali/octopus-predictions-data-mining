from datetime import datetime
import pickle
import pandas as pd

leagueId="6250d82b81afe4381753aefa"

with open(f'src/models/{leagueId}.params.pkl', 'rb') as handle:
    params = pickle.load(handle)
    
classifiers= pd.read_pickle(f'src/models/{leagueId}.classifiers.pkl')  





homeTeam='tunisia'
awayTeam='france'
date='2021-09-05T16:00:00.000Z'
date=datetime.strptime(date,'%Y-%m-%dT%H:%M:%S.%fZ').toordinal()
match_row=[]

#normalising date
date=(date-params['scaler_data_min_'])/(params['scaler_data_max_']-params['scaler_data_min_'])



for column in params['data_columns']:
    if(column=='date'):
        match_row.append(date)
    elif(column==f'homeTeam_{homeTeam}'):
        match_row.append(1)
    elif(column==f'awayTeam_{awayTeam}'):
        match_row.append(1)
    else:
        match_row.append(0)

data_to_predict=pd.DataFrame([match_row],columns=params['data_columns'])

predictions=[]

for index,classifier in classifiers.iterrows():
    prediction=[]
    for target_label in params['targets_keys']:
        prediction.append(classifier[target_label].predict(data_to_predict))
    predictions.append(prediction)


predictions=pd.DataFrame(predictions,columns=params['targets_keys'])

print(predictions)