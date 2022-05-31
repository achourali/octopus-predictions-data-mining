import requests
import json


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




if __name__ == "__main__":
    matches = getMatches('6250d82b81afe4381753aefa')
    matches = cleanMatches(matches)
    # target=createTarget(matches)
    print(matches[0])
