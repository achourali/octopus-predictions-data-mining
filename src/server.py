from predict_match import predict_match
from flask import Flask
import json

app = Flask(__name__)


@app.route('/')
def hello():
    leagueId = "6250d82b81afe4381753aefa"
    homeTeam = 'tunisia'
    awayTeam = 'france'
    date = '2022-11-30T15:00:00.000Z'

    print('test***************************')
    print(predict_match(leagueId, homeTeam, awayTeam, date))
    return json.dumps(predict_match(leagueId, homeTeam, awayTeam, date))

