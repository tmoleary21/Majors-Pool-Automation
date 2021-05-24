from Scraping_ESPN_Golf import *
from pathlib import Path

def readResults(csv):
    header = ['First Name', 'Last Name', 'Golfer 1', 'Earnings 1', 'Golfer 2', 'Earnings 2', 'Golfer 3', 'Earnings 3', 'Total Earnings', 'Tie-Breaker']
    results = pd.read_csv(csv, usecols=range(0, 9), names=header)
    return results.to_numpy().tolist()


prevTournaments = [str(x) for x in [*Path().iterdir()] if str(x).endswith('.csv') and str(x) != 'Majors Pool.csv']  #list of csv files in current directory
print('Select the tournaments to compute. Just list the numbers like 1234')
print(''.join([str(i+1) + ' - ' + prevTournaments[i] + '\n' for i in range(len(prevTournaments))]))
selected = input()
csvs = [prevTournaments[i] for i in range(len(prevTournaments)) if str(i+1) in selected]
# print(csvs)
# print( str( readResults(csvs[0]) ).replace('],','],\n') )
totals = {}
for csv in csvs:
    addedPeople = []
    for person in readResults(csv)[1:]:
        # print(str(person))
        if person[0:2] not in addedPeople:  # ensuring no duplicate responses in one tournament
            if (person[0]+' '+person[1]) not in totals:
                totals[person[0].strip()+' '+person[1].strip()] = person[8]
            else:
                totals[person[0].strip()+' '+person[1].strip()] = str(int(totals[person[0].strip()+' '+person[1].strip()]) + int(person[8]))
            addedPeople.append(person[0:2])

data = sorted([[x, totals[x]] for x in totals], key=lambda a:int(a[1]), reverse=True)
print(data)
print('\n'.join([' : '.join(x) for x in data]))  # Definitely too complex, but prints leaderboard

header = ['Name', 'Total Earnings']
df = pd.DataFrame(data=data,index=range(1,len(data)+1), columns=header)
print(df)
df.to_csv('runningStandings.csv', index=False, header=True)

