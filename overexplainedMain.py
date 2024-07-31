from dotenv import load_dotenv
import os
import requests
import json
import sqlite3
import time
import csv

load_dotenv()

api_key = os.getenv("Key")
api_SummonerURL = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
api_MatchURL = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
api_SpecMatchURL = "https://europe.api.riotgames.com/lol/match/v5/matches/"

class Summoner:
    def __init__(self, summonerID, summonerName, championName, summonerRole, teamId, win):
        self.summonerID = str(summonerID)
        self.summonerName = str(summonerName)
        #self.encounters = int(encounters)
        self.championName = str(championName)
        #self.selfChamp = str(selfChamp)
        #self.sameTeam = bool(sameTeam)
        #self.selfWin = bool(selfWin)
        self.teamId = str(teamId)
        self.summonerRole = str(summonerRole)
        #self.selfRole = str(selfRole)
        self.win = bool(win)

def getGames(username):
    targetSummoner = username
    targetSummonerPUUID = 'q'
    targetServer = 'EUN1'
    targetGameID = 0
    targetMatchID = targetServer + "_" + str(targetGameID)
    epochTime = int(time.time())
    epochLimit = 1623844800
    matchList = []

    r = requests.get(api_SummonerURL+targetSummoner+'?api_key='+api_key)
    time.sleep(0.8)
    summonerJSON = json.loads(r.text)
    targetSummonerPUUID = summonerJSON['puuid']
    print(targetSummonerPUUID)

    data={
        'endTime': epochTime, 'type': 'ranked', 'start': 0, 'count':100, 'api_key': api_key
    }

    r = requests.get(api_MatchURL+targetSummonerPUUID+"/ids", params=data)
    time.sleep(0.8)

    #print(data)
    #print(r.url)
    #print (r.text)

    while epochTime > epochLimit:
    #for a in range(0,2):
        data["endTime"] = epochTime
        r = requests.get(api_MatchURL+targetSummonerPUUID+"/ids", params=data)
        time.sleep(0.8)
        matchJSON = json.loads(r.text)
        for match in matchJSON:
            if match not in matchList:
                matchList.append(match)
        if len(matchJSON)>0 :
            print(matchJSON)
            lastMatch = matchJSON[-1]
            r = requests.get(api_SpecMatchURL+lastMatch+'?api_key='+api_key)
            if (r.status_code != 200):
                i = 2
                while (r.status_code != 200 and i < 101):
                    print("not found, "+lastMatch)
                    lastMatch = matchJSON[len(matchJSON)-i]
                    r = requests.get(api_SpecMatchURL+lastMatch+'?api_key='+api_key)
                    time.sleep(0.5)
                    i += 1
                if i > 100:
                    break
            time.sleep(0.8)
            lastMatchJSON = json.loads(r.text)
            print(lastMatchJSON)
            if epochTime != int(lastMatchJSON["info"]["gameEndTimestamp"]/1000):
                epochTime = int(lastMatchJSON["info"]["gameEndTimestamp"]/1000)
            else:
                break
        else:
            break
    for match in matchList:
        print(match)
    with open(r'C:\Users\prefe\Desktop\riotProject\matches.txt', "w") as outfile:
        for match in matchList:
            outfile.write(match+"\n")

def getGameSums(matchID):
    summonersList = dict()
    testList = ['sum1', 'sum2', 'sum3', 'sum4', 'sum5']
    r = requests.get(api_SpecMatchURL+matchID+'?api_key='+api_key)
    time.sleep(0.5)
    testList.clear()
    testListJSON = json.loads(r.text)
    for summoner in testListJSON["info"]["participants"]:
        testList.append(summoner["summonerName"])
    for summoner in testList:
        if summoner not in summonersList.keys():
            summonersList[summoner] = 1
        else:
            summonersList[summoner] += 1
    print(summonersList)
    print(testList)
summonersList = []
def getAllGameSums():
    matchesfile = open(r"C:\Users\prefe\Desktop\riotProject\matches.txt", "r")
    matchesList = []
    tempSummonersList = []
    Lines = matchesfile.readlines()
    count = 0
    for line in Lines:
        count += 1
        matchesList.append(line.strip())
    for match in matchesList:
        r = requests.get(api_SpecMatchURL+match+'?api_key='+api_key)
        time.sleep(1.2)
        tempSummonersList.clear()
        summonersListJSON = json.loads(r.text)
        print(summonersListJSON)
        for summoner in summonersListJSON["info"]["participants"]:
            tempSummonersList.append(summoner["summonerId"])
            print(tempSummonersList)
        for summoner in tempSummonersList:
            if summoner not in summonersList.keys():
                summonersList[summoner] = 1
            else:
                summonersList[summoner] += 1
            print(summoner)
        print("Finished " + match)
    writeSumDict(summonersList)
def getAllGameDetails():
    matchesfile = open(r"C:\Users\prefe\Desktop\riotProject\matches.txt", "r")
    matchesList = []
    tempSummonersList = []
    Lines = matchesfile.readlines()
    count = 0
    for line in Lines:
        count += 1
        matchesList.append(line.strip())
    for match in matchesList:
        r = requests.get(api_SpecMatchURL+match+'?api_key='+api_key)
        time.sleep(1.2)
        tempSummonersList.clear()
        summonersListJSON = json.loads(r.text)
        print(summonersListJSON)
        for summoner in summonersListJSON["info"]["participants"]:
            if summoner["summonerName"] == 'Senshougahara':
                selfSummoner = Summoner(summoner["summonerId"], summoner["summonerName"], summoner["championName"], summoner["teamId"], summoner["individualPosition"], summoner["win"])
            else:
                summonerSummoner = Summoner(summoner["summonerId"], summoner["summonerName"], summoner["championName"], summoner["teamId"], summoner["individualPosition"], summoner["win"])
                tempSummonersList.append(summonerSummoner)
            print(tempSummonersList)
        for summoner in tempSummonersList:
            summoner.selfChamp = selfSummoner.championName
            if (selfSummoner.teamId == summoner.teamId):
                summoner.sameTeam = True
            else:
                summoner.sameTeam = False
            summoner.selfRole = selfSummoner.summonerRole
            summoner.selfChamp = selfSummoner.championName
            if (summoner.sameTeam and summoner.win):
                summoner.selfWin = True
###########
        summonersList.append(tempSummonersList)
#        for summoner in tempSummonersList:
#            if summoner not in summonersList.keys():
#                summonersList[summoner] = 1
#            else:
#                summonersList[summoner] += 1
#            print(summoner)
        print("Finished " + match)
#    writeSumDict(summonersList)
#    with io.open(r'C:\Users\prefe\Desktop\riotProject\summoners.csv', "w", encoding='utf8') as outfile:
#        for summoner in summonersList:
#            outfile.write(str(summoner)+"\n")
#    for summoners in summonersList:
#        for summoner in summoners:
#            print(summoner.summonerName)
def writeSumDict(summonersDict):
    with open(r'C:\Users\prefe\Desktop\riotProject\summoners.csv', 'w', encoding='UTF8', newline='') as f:
        fieldnames1 = ['Game Details', '', '', '', '', '', '', '', '', '', 'Statistics']
        fieldnames2 = ['Summoner ID', 'Summoner Name', 'Encounter', 'SumChamp', 'MyChamp', 'Same Team', 'MyWin','MyRole','SumRole','Summoner Name','Total Encounters','WinrateSameTeam','WinrateOpTeam','Main Role','(personal) Main Role']
        tempList = list(summonersDict.items())
        writer = csv.writer(f)
        writer.writerow(fieldnames1)
        writer.writerow(fieldnames2)
        for summoner in tempList:   
            writer.writerow(summoner)

#getAllGameSums()

def sumsDB():
    conn = sqlite3.connect(r'C:\Users\prefe\Desktop\riotProject\summoners.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS summonerStats
                (summonerID TEXT, summonerName TEXT, summonerChamp TEXT, selfChamp TEXT, sameTeam BOOLEAN, selfWin BOOLEAN, summonerRole TEXT, selfRole TEXT, win BOOLEAN)
                ''')
    #summonersStats = [
    #    ('4389248932', 'Nevermind', '1', 'Ahbar', 'Abdul', '1', '1', 'Supp', 'Top'),
    #    ('6554648932', 'Nevermind', '2', 'Ahbar', 'Abdul', '0', '1', 'ADC', 'Top'),
    #    ('43765748932', 'Nevermind', '3', 'Ahbar', 'Abdul', '0', '0', 'Supp', 'Top'),
    #]
    addSummoner = ("INSERT INTO summonerStats "
                           "(summonerID, summonerName, summonerChamp, selfChamp, sameTeam, selfWin, summonerRole, selfRole, win) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
    for summoners in summonersList:
        for summoner in summoners:
            cur.execute(addSummoner, (summoner.summonerID, summoner.summonerName, summoner.championName, summoner.selfChamp, summoner.sameTeam, summoner.selfWin, summoner.summonerRole, summoner.selfRole, summoner.win))
    #summonerStats = [
    #    f"('{valoare}', '{valoare2}, '{valoare3}, '{valoare4}, '{valoare5})"
    #]
    #cur.executemany('''
    #                INSERT INTO summonerStats (summonerID, summonerName, encounters, summonerChamp, selfChamp, sameTeam, selfWin, summonerRole, selfRole) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    #                ''', summonersStats)
    conn.commit()
    cur.close()
    conn.close()

def testCase():
    #getGames('Senshougahara')
    #getGameSums('EUN1_3484272913')
    #getAllGameSums()
    getAllGameDetails()
    sumsDB()
testCase()

#getGames('Senshougahara')
#getGameSums('EUN1_3406804296')
#get_sums('EUN1_3109659533')
#
#
#
#f=open(r'C:\Users\prefe\Desktop\riotProject\example.json')
#data = json.load(f)
#
#for i in range(0,10):
#    print(data["info"]["participants"][i]["summonerName"])
#    if (data["info"]["participants"][i]["summonerName"]) not in summonersList:
#        summonersList.append(data["info"]["participants"][i]["summonerName"])
#
#f.close()
#
#con = sqlite3.connect("summoners.db")
#cur = con.cursor()
#
#for i in summonersList:
#    cur.execute("""SELECT name
#            FROM summoner
#            WHERE name=?""", (i))
#    result = cur.fetchone()
#    if result:
#        cur.execute("""SELECT count
#                    FROM summoner""")
#        
#    else:
#        cur.execute("INSERT INTO summoner VALUES (?)", (i))
#        con.commit()
#
#cur.execute("CREATE TABLE summoner(name, count)")
#res = cur.execute("SELECT name FROM sqlite_master")
#res.fetchone()
#cur.execute("""
#            INSERT INTO summoner VALUES
#            ('testname', 0),
#            ('testname2', 1)
#            """)
#con.commit()
#res = cur.execute("SELECT count FROM summoner")
#for row in cur.execute("SELECT count FROM summoner ORDER BY count"):
#    print(row)
#
#data = [
#    ("summoner1", 0),
#    ("summoner2", 1),
#    ("summoner3", 2),
#]
#cur.executemany("INSERT INTO summoner VALUES(?, ?)", data)
#con.commit()