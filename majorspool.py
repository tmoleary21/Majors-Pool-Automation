from Scraping_ESPN_Golf import *
from pathlib import Path

prevTournaments = [str(x) for x in [*Path().iterdir()] if str(x).endswith('.csv') and str(x) != 'Majors Pool.csv']  #list of csv files in current directory
print('Select the tournaments that were a part of this majors pool')
print(''.join([str(i+1) + ' - ' + prevTournaments[i] + '\n' for i in range(len(prevTournaments))]))
csvs = [input(), input(), input(), input()]