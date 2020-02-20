import urllib.request
def getPlayerInfo(playerName):
    url = 'https://www.espn.com/golf/rankings'
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    start = rhtml.index('"current":13')  #will need to be changed by player instead of this
    
    braceCount = 1
    i = start
    while braceCount != 0:
        if rhtml[i] == '{':
            braceCount += 1
        if rhtml[i] == '}':
            braceCount -= 1
        i += 1
    end = i
    
    infoText = rhtml[start-1:end]
    
    #Want First Name, Last Name, ID ... ANYTHING ELSE?
    firstNameStart = infoText.index('"firstName":') + 13
    firstNameEnd = infoText[firstNameStart:].index('"')
    
    lastNameStart = infoText.index('"lastName":') + 12
    lastNameEnd = infoText[lastNameStart:].index('"')
    
    idStart = infoText.index('"id":')+6
    idEnd = infoText[idStart:].index('"')
    
    info = {'first': infoText[firstNameStart:firstNameStart + firstNameEnd], 
            'last': infoText[lastNameStart:lastNameStart + lastNameEnd], 
            'id': infoText[idStart:idStart + idEnd]}
    
    return info

print(getPlayerInfo(''))




def getPlayerScores(info):
    url = 'http://www.espn.com/golf/player/_/id/' + info.get('id') + '/' + info.get('firstName') + '-' + info.get('lastName')
    html = urllib.request.urlopen(url).read()
    rhtml = ''.join([chr(n) for n in html])
    #TODO: needs to find the final score from tournament and earnings.
