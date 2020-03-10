import pandas as pd
import numpy
import urllib.request


def readResponses():
    names = ['Timestamp', 'First Name', 'Last Name', 'Golfer 1', 'Golfer 2', 'Golfer 3', 'Final Score']
    responses = pd.read_csv("Majors Pool.csv", usecols=range(1,7), names=names)
    return responses.to_numpy().tolist()


def getPlayerLink(playerLastName):
    url = 'https://www.espn.com/golf/rankings'
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    start = rhtml.index(playerLastName.lower())
    linkEnd = start + rhtml[start:].index('"')

    while rhtml[start] != '"':
        start -= 1
    return rhtml[start+1:linkEnd]


print(getPlayerLink("koepka"))


def getPlayerEarnings(playerLastName):
    url = getPlayerLink(playerLastName)
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])

    #TODO: needs to find the final score from tournament and earnings.


responses = readResponses()

tally = [[]]

for i in range(1,len(responses)):
    tally[i] = responses[:3]
    tally[i][3] = getPlayerEarnings(responses[2].split()[1])
    tally[i][4] = responses[3]
    tally[i][3] = getPlayerEarnings(responses[3].split()[1])
    tally[i][6] = responses[4]
    tally[i][3] = getPlayerEarnings(responses[4].split()[1])
