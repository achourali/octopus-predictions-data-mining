import requests
import json


def getMatches(leagueId):

    r = requests.get(f'http://localhost:3000/football/{leagueId}/all/matches')
    return json.loads(r.text)


def cleanMatches(matches):
    for match in matches:
        del(match['_id'])
        del(match['date'])
        del(match['flashscoreId'])
        del(match['round'])
        del(match['season'])
        del(match['createdAt'])
        del(match['updatedAt'])
        del(match['__v'])
        match['homeTeam'] = match['homeTeam']['name']
        match['awayTeam'] = match['awayTeam']['name']
        match['homeTeamGoals'] =len(list(filter(lambda goal: goal['homeTeam'] == True, match['goals'])))
        match['awayTeamGoals'] =len(list(filter(lambda goal: goal['homeTeam'] == False, match['goals'])))
        del(match['goals'])

    return




if __name__ == "__main__":
    matches = getMatches('6250d75e81afe4381753aade')
    cleanMatches(matches)
    print(matches[0])
