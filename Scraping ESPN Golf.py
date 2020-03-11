import pandas as pd
import urllib.request
import re


def readResponses():
    names = ['Timestamp', 'First Name', 'Last Name', 'Golfer 1', 'Golfer 2', 'Golfer 3', 'Final Score']
    responses = pd.read_csv("Majors Pool.csv", usecols=range(1,7), names=names)
    return responses.to_numpy().tolist()

def accessRankings(): #Just for accessing the rankings site, so it can be accessed only once.
    url = 'https://www.espn.com/golf/rankings'
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    return rhtml

def getPlayerLink(rhtml, playerLastName):
    start = rhtml.index(playerLastName.lower())
    linkEnd = start + rhtml[start:].index('"')

    while rhtml[start] != '"':
        start -= 1
    return rhtml[start+1:linkEnd]


#print(getPlayerLink(accessRankings(),"McIlroy"))


def getScores(url): #Gets the player earnings from the player's profile site
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    start = rhtml.index('Recent 2020 PGA Tour Tournaments')
    start = rhtml.index('<td align="left">\n', start) + 18 #MIGHT NEED TO BE CHANGED. SEEMS FLIMSY
    end = start + rhtml[start:].index('</table>')

    tournaments = rhtml[start:end].split('<td align="left">')
    tournaments = [re.split(r'[ ]*[|]+[ ]*', re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', t))) for t in tournaments]

    info = []
    for i in range(1,len(tournaments),2):
        temp = []
        for j in range(len(tournaments[i])):
            if j == 1:
                temp.append(tournaments[i][j])
            if '(' in tournaments[i][j]:
                temp.append(0 if 'E' in tournaments[i][j] else int(tournaments[i][j][1:-1]))
            if '$' in tournaments[i][j]:
                temp.append(int(tournaments[i][j][1:].replace(',','')))
        info.append(temp)

    # for i in info: #Just for debugging
    #     print(i)

    return info




responses = readResponses()
print(str(responses) + '\n')

rankingsHTML = accessRankings()

tournament = ''
tally = []
for i in range(1,len(responses)):
    tally.append(responses[i][0])
    tally.append(responses[i][1])
    tally.append(getScores(getPlayerLink(rankingsHTML, responses[i][2].split()[1])))
    tally.append(getScores(getPlayerLink(rankingsHTML, responses[i][3].split()[1])))
    tally.append(getScores(getPlayerLink(rankingsHTML, responses[i][4].split()[1])))
    tally.append(responses[i][5])

for t in tally:
    print(t)


