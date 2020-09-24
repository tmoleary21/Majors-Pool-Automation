import pandas as pd
import urllib.request
import re


def readResponses():
    names = ['Timestamp', 'First Name', 'Last Name', 'Golfer 1', 'Golfer 2', 'Golfer 3', 'Final Score']
    responses = pd.read_csv("Majors Pool.csv", usecols=range(1, 7), names=names)
    return responses.to_numpy().tolist()


def accessLeaderboard(yearXTRAURL=''):
    url = 'https://www.espn.com/golf/leaderboard' + yearXTRAURL
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    return rhtml

def accessSpecificLeaderboard(mainLeaderboardHtml, tournament):
    i = mainLeaderboardHtml.index('value="Selected">' + tournament + '</option>')
    start = i
    while(mainLeaderboardHtml[start-1:start+1] != '"/'):
        start -= 1
    end = mainLeaderboardHtml[start:i].index('"')

    url = 'https://www.espn.com' + mainLeaderboardHtml[start:start+end]
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    rhtml = rhtml[rhtml.index('<table'):]
    rhtml = rhtml[:rhtml.index('</table>')]
    return rhtml


def getEarnings(player, tableHtml):  # Gets the player earnings from the tournament's html table
    try:
        start = tableHtml.index(player)
    except(ValueError):
        return "NIT"
    end = tableHtml[start:].index('</tr>')
    try:
        start2 = start + tableHtml[start:start+end].index('$')
    except(ValueError):
        return 0
    end = tableHtml[start2:start+end].index('</td>')
    return int(tableHtml[start2+1:start2+end].replace(',',''))


def getTournaments(rhtml):  # Gets a list of recent tournaments. Pass in leaderboard rhtml. Only gives tournaments in the currrent year/ golf season. Ex. 2020-21. Whatever is default on the page
    start = rhtml.index('Tournaments')
    end = start + rhtml[start:].index('</div>')
    tournaments = rhtml[start:end].split('value="Selected">')
    tournaments = [tournaments[i][:tournaments[i].index('<')] for i in range(1, len(tournaments))]
    return tournaments


def getWinnerScore(rhtml):  # Grabs the selected tournament's winner's score to be compared with guesses
    start = rhtml.index('AnchorLink leaderboard_player_name')
    start = start + rhtml[start:].index('<td class="Table__TD">') + 22
    end = start + rhtml[start:start + 10].index('<')
    if rhtml[start:end] == 'E':
        return 0
    return int(rhtml[start:end])


def decideTie(tally, winnerIndices, tournamentWinnerScore):
    winner = winnerIndices[0]
    for i in range(1, len(winnerIndices)):
        if abs(int(tally[winnerIndices[i]][9]) - tournamentWinnerScore) < abs(
                int(tally[winner][9]) - tournamentWinnerScore):
            winner = winnerIndices[i]
    return winner


responses = readResponses()
# print(str(responses) + '\n')


leaderboardHTML = accessLeaderboard()
# leaderboardHTML = accessLeaderboard('/_/tournamentId/401219793/season/2020') #To test 2019-20


# Choose Tournament
tournaments = getTournaments(leaderboardHTML)
for i in range(min(15, len(tournaments))):
    print(str(i + 1) + ' - ' + tournaments[i])
tournament = tournaments[int(input()) - 1]
# print(tournament)
tournamentHtml = accessSpecificLeaderboard(leaderboardHTML, tournament)

winnerIndices = [0]
tally = []
for i in range(1, len(responses)):
    sum = 0
    temp = []
    temp.append(responses[i][0])  # ......................................................................First Name
    temp.append(responses[i][1])  # ......................................................................Last Name
    temp.append(responses[i][2])  # ......................................................................Golfer 1 Name
    temp.append(getEarnings(responses[i][2], tournamentHtml))  # .........................................Golfer 1 Score
    sum += temp[3] if temp[3] != "NIT" else 0
    temp.append(responses[i][3])  # ......................................................................Golfer 2 Name
    temp.append(getEarnings(responses[i][3], tournamentHtml))  # .........................................Golfer 2 Score
    sum += temp[5] if temp[5] != "NIT" else 0
    temp.append(responses[i][4])  # ......................................................................Golfer 3 Name
    temp.append(getEarnings(responses[i][4], tournamentHtml))  # .........................................Golfer 3 Score
    sum += temp[7] if temp[7] != "NIT" else 0
    temp.append(sum)  # ..................................................................................Sum of earnings
    temp.append(int(responses[i][5]))  # ......................................................................Score guess
    tally.append(temp)
    if i > 1:
        if sum == tally[winnerIndices[0]][8]:
            winnerIndices.append(i - 1)
        if sum > tally[winnerIndices[0]][8]:
            winnerIndices = [i - 1]

# for t in tally:
#     print(t)

#print(winnerIndices)
winnerIndex = decideTie(tally, winnerIndices, getWinnerScore(tournamentHtml))
print('\nWINNER: ' + str(tally[winnerIndex]))

tally = sorted(tally, key=lambda a : a[8], reverse=True)

for i in range(len(tally)):
    tally[i] = [t[2] if type(t) == list and len(t) == 3 else 'NO DATA' if type(t) == list else t for t in tally[i]]

header = ['First Name', 'Last Name', 'Golfer 1', 'Earnings 1', 'Golfer 2', 'Earnings 2', 'Golfer 3', 'Earnings 3', 'Total Earnings', 'Tie-Breaker']

df = pd.DataFrame(tally, index=range(1,len(tally)+1), columns=header)
df.to_csv(tournament + '.csv', index=False, header=True)
print(df)

input("Open <tournament>.csv to see results. Press the ENTER key to exit")