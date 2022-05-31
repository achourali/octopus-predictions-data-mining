import requests
import json
import pandas as pd


def getMatches(leagueId):

    r = requests.get(f'http://localhost:3000/football/{leagueId}/all/matches')
    return json.loads(r.text)


def cleanMatches(matches):
    cleanData = []
    for match in matches:
        cleanMatch = {}
        if(match['finished'] == False):
            matches.remove(match)
            continue
        cleanMatch['homeTeam'] = match['homeTeam']['name']
        cleanMatch['awayTeam'] = match['awayTeam']['name']
        cleanMatch['homeTeamGoals'] = len(
            list(filter(lambda goal: goal['homeTeam'] == True, match['goals'])))
        cleanMatch['awayTeamGoals'] = len(
            list(filter(lambda goal: goal['homeTeam'] == False, match['goals'])))
        cleanData.append(cleanMatch)

    return cleanData


def restructuringData(matches):
    homeTeam=[]
    awayTeam=[]
    for match in matches:
        homeTeam.append(match['homeTeam'])
        awayTeam.append(match['awayTeam'])
    return pd.DataFrame({'homeTeam':homeTeam,'awayTeam':awayTeam})


def createTarget(matches):
    target = []
    for match in matches:
        if(match['homeTeamGoals'] > match['awayTeamGoals']):
            target.append('home')
        elif(match['homeTeamGoals'] < match['awayTeamGoals']):
            target.append('away')
        else:
            target.append('draw')
    return target


if __name__ == "__main__":
    matches = getMatches('6250d75e81afe4381753aade')
    matches = cleanMatches(matches)
    target = createTarget(matches)
    print(restructuringData(matches))
    

