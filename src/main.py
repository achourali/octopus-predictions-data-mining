import requests
import json
import pandas as pd
from sklearn import naive_bayes
from sklearn.model_selection import train_test_split


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
    homeTeam = []
    awayTeam = []
    for match in matches:
        homeTeam.append(match['homeTeam'])
        awayTeam.append(match['awayTeam'])

    df = pd.DataFrame({'homeTeam': homeTeam, 'awayTeam': awayTeam})
    return pd.get_dummies(df)


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


def average_score(classifier, data, target):
    sum = 0
    cycles = 1000

    for i in range(1, cycles):

        train_data, test_data, train_target, test_target = train_test_split(
            data, target, test_size=0.2)
        classifier.fit(train_data, train_target)
        sum += classifier.score(test_data, test_target)
        
    return sum/cycles


if __name__ == "__main__":
    matches = getMatches('6250d75e81afe4381753aade')
    matches = cleanMatches(matches)
    target = createTarget(matches)
    data = restructuringData(matches)

    nb_clf = naive_bayes.MultinomialNB(fit_prior=True)

    print(average_score(nb_clf, data, target))
