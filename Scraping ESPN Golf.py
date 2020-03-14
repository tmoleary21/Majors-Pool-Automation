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


def getPlayerLink(rhtml, playerLastName): #Grabs the link for the player's profile site from the rankings site
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


def accessTournaments(): #Accesses the tournaments page so it is only accessed once
    url = 'https://www.espn.com/golf/leaderboard/_/tournamentId/401155428'
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    return rhtml


def getTournaments(rhtml): #Gets a list of recent tournaments
    start = rhtml.index('Tournaments')
    end = start + rhtml[start:].index('</div>')
    tournaments = rhtml[start:end].split('value="Selected">')
    tournaments = [tournaments[i][:tournaments[i].index('<')] for i in range(1,len(tournaments))]
    return tournaments


def getWinnerScore(tournamentHTML, tournament): #Grabs the selected tournament's winner's score to be compared with guesses
    linkEnd = tournamentHTML.index(tournament) - 19
    linkStart = linkEnd-1
    while tournamentHTML[linkStart] != '"':
        linkStart -= 1

    url = 'https://www.espn.com' + tournamentHTML[linkStart+1:linkEnd]
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    start = rhtml.index('AnchorLink leaderboard_player_name')
    start = start + rhtml[start:].index('<td class="Table__TD">') + 22
    end = start + rhtml[start:start+10].index('<')
    if rhtml[start:end] == 'E':
        return 0
    return int(rhtml[start:end])


def decideTie(tally, winnerIndices, tournamentWinnerScore):
    winner = winnerIndices[0]
    for i in range(1,len(winnerIndices)):
        if abs(int(tally[winnerIndices[i]][9]) - tournamentWinnerScore) < abs(int(tally[winner][9]) - tournamentWinnerScore):
            winner = winnerIndices[i]
    return winner

responses = readResponses()
#print(str(responses) + '\n')

rankingsHTML = accessRankings()
tournamentsHTML = accessTournaments()

#Choose Tournament
tournaments = getTournaments(tournamentsHTML)
for i in range(15):
    print(str(i+1) + ' - ' + tournaments[i])
tournament = tournaments[int(input())-1]

winnerIndices = [0]
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
        if sum == tally[winnerIndices[0]][8]:
            winnerIndices.append(i-1)
        if sum > tally[winnerIndices[0]][8]:
            winnerIndices = [i-1]

for t in tally:
    print(t)

#print(winnerIndices)
if len(winnerIndices) > 1:
    winnerIndex = decideTie(tally, winnerIndices, getWinnerScore(tournamentsHTML, tournament))
    print('\nWINNER: ' + str(tally[winnerIndex]))
else:
    winnerIndex = winnerIndices[0]
    print('\nWINNER: ' + str(tally[winnerIndices[0]]))

temp = tally[winnerIndex]
tally[winnerIndex] = tally[0]
tally[0] = temp

for i in range(len(tally)):
    tally[i] = [t[2] if type(t) == list and len(t) == 3 else 'NO DATA' if type(t) == list else t for t in tally[i]]

header = ['First Name', 'Last Name', 'Golfer 1', 'Earnings 1', 'Golfer 2', 'Earnings 2', 'Golfer 3', 'Earnings 3', 'Total Earnings', 'Tie-Breaker']

df = pd.DataFrame(tally, index=range(1,len(tally)+1), columns=header)
df.to_csv(tournament + '.csv', index=False, header=True)
print(df)
