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

def getScores(url, tournament): #Gets the player earnings from the player's profile site
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    start = rhtml.index('Recent 2020 PGA Tour Tournaments')
    start = rhtml.index('<td align="left">\n', start) + 18 #MIGHT NEED TO BE CHANGED. SEEMS FLIMSY
    end = start + rhtml[start:].index('</table>')

    tournaments = rhtml[start:end].split('<td align="left">')
    tournaments = [re.split(r'[ ]*[|]+[ ]*', re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', t))) for t in tournaments]

    info = []
    for i in range(1,len(tournaments),2):
        temp = ['', 0, 0]
        for j in range(len(tournaments[i])):
            if j == 1:
                temp[0] = tournaments[i][j]
            if '(' in tournaments[i][j]:
                temp[1] = 0 if 'E' in tournaments[i][j] else int(tournaments[i][j][1:-1])
            if 'Withdrawn' in tournaments[i][j]:
                temp[1] = 'Withdrawn'
            if 'Missed Cut' in tournaments[i][j]:
                temp[1] = 'Missed Cut'
            if 'Disqualified' in tournaments[i][j]:
                temp[1] = 'Disqualified'
            if '$' in tournaments[i][j]:
                temp[2] = int(tournaments[i][j][1:].replace(',', ''))
        info.append(temp)

    # for i in info: #Just for debugging
    #     print(i)
    def findIndex():
        for i in range(len(info)):
            if tournament in info[i]:
                return i
        return None

    index = findIndex()
    if index == None:
        return []
    return info[index]

def accessTournaments():
    url = 'https://www.espn.com/golf/leaderboard/_/tournamentId/401155428'
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    return rhtml

def getTournaments(rhtml):
    start = rhtml.index('Tournaments')
    end = start + rhtml[start:].index('</div>')
    tournaments = rhtml[start:end].split('value="Selected">')
    tournaments = [tournaments[i][:tournaments[i].index('<')] for i in range(1,len(tournaments))]
    return tournaments

def getWinnerScore(tournamentHTML, tournament): #PROBLEM. ERROR WHEN FINDING WEB PAGE.
    linkEnd = tournamentHTML.index(tournament) - 19
    linkStart = linkEnd-1
    while tournamentHTML[linkStart] != '"':
        linkStart -= 1
    print(tournamentHTML[linkStart+1:linkEnd])

    url = 'https://www.espn.com' + tournamentHTML[linkStart:linkEnd]
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])

getWinnerScore(accessTournaments(),'Arnold Palmer Invitational Pres. By Mastercard')




responses = readResponses()
print(str(responses) + '\n')

rankingsHTML = accessRankings()
tournamentsHTML = accessTournaments()

#Choose Tournament
tournaments = getTournaments(tournamentsHTML)
for i in range(6):
    print(str(i+1) + ' - ' + tournaments[i])
tournament = tournaments[int(input())-1]

winnerIndex = 0
tally = []
for i in range(1,len(responses)):
    sum = 0
    temp = []
    temp.append(responses[i][0])
    temp.append(responses[i][1])
    temp.append(responses[i][2])
    temp.append(getScores(getPlayerLink(rankingsHTML, responses[i][2].split()[1]), tournament))
    sum += temp[3][2] if len(temp[3]) > 2 else 0
    temp.append(responses[i][3])
    temp.append(getScores(getPlayerLink(rankingsHTML, responses[i][3].split()[1]), tournament))
    sum += temp[5][2] if len(temp[5]) > 2 else 0
    temp.append(responses[i][4])
    temp.append(getScores(getPlayerLink(rankingsHTML, responses[i][4].split()[1]), tournament))
    sum += temp[7][2] if len(temp[7]) > 2 else 0
    temp.append(sum)
    temp.append(responses[i][5])
    tally.append(temp)
    if i > 1:
        winnerIndex = i-1 if sum > tally[i-2][8] else winnerIndex

for t in tally:
    print(t)


print('WINNER: ' + str(tally[winnerIndex]))
