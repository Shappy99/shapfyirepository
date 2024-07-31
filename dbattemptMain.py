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

def getAllGameSums():
    matchesfile = open(r"C:\Users\prefe\Desktop\riotProject\matches.txt", "r")
    matchesList = []
    summonersList = dict()
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
            tempSummonersList.append(summoner["summonerName"])
            print(tempSummonersList)
        for summoner in tempSummonersList:
            if summoner not in summonersList.keys():
                summonersList[summoner] = 1
            else:
                summonersList[summoner] += 1
            print(summoner)
        print("Finished " + match)
    writeSumDict(summonersList)
#    with io.open(r'C:\Users\prefe\Desktop\riotProject\summoners.csv', "w", encoding='utf8') as outfile:
#        for summoner in summonersList:
#            outfile.write(str(summoner)+"\n")
def writeSumDict(summonersDict):
    with open(r'C:\Users\prefe\Desktop\riotProject\summoners.csv', 'w', encoding='UTF8', newline='') as f:
        fieldnames = ['Summoner', 'Count']
        tempList = list(summonersDict.items())
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for summoner in tempList:   
            writer.writerow(summoner)

getAllGameSums()
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