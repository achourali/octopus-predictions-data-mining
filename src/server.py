from predict_match import predict_match
from flask import Flask
from flask import jsonify
from flask import request


app = Flask(__name__)


@app.route('/',methods=['POST'])
def hello():
    return jsonify(
        predict_match(
            request.get_json()['leagueId'],
            request.get_json()['homeTeam'],
            request.get_json()['awayTeam'],
            request.get_json()['date']
            )
        )

