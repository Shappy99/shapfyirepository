### main.py

## importing libraries

#Used to load API Key from .env
from dotenv import load_dotenv
#Used to access files in directory
import os
#Used to make API calls
import requests
#Used to convert/work with JSON type files
import json
#Used to access and make calls to SQLite Database
import sqlite3
#Used to wait time in order to not get timed out when making API calls or to grab today's date to use in certain API calls
import time
#Used to convert data into a CSV type of file to use in Excel
import csv
#Used to create an interface for easier interactions
#import PySimpleGUI
#Test - used to write files with proper encoding
import io

## declaring variables

#Load the .env file
load_dotenv()
#Grab the API key from the .env file
api_key = os.getenv("Key")
#Format the string to add it directly to the API call link
api_keyF = '?api_key='+api_key

#Save API urls that will be used to make calls
#1. Grab information about a summoner by summoner name
api_SummonerURL = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
#2. Grab matches IDs played by a summoner by the summoner PUUID (grabbed from 1.)
api_MatchURL = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
#3. Grab information about a particular game by the Match ID (grabbed from 2.)
api_SpecMatchURL = "https://europe.api.riotgames.com/lol/match/v5/matches/"

## declaring classes

#Defining classes for the type of tables we are going to use in the database
#We are going to have different classes:
#1. Summoner -> Saves information about a particular summoner
class Summoner:
    def __init__(self):
        pass
#2. Summoner Encounter -> Saves information about a particular match played with a particular summoner
class summonerEncounter:
    def __init__(self):
        pass
#3. Match -> Saves information about a particular match
class Match:
    def __init__(self):
        pass
#4. Statistics -> Saves information about overall statistics based on summoner encounters
class summonerStatistics:
    def __init__(self):
        pass

##Defining functions

#We are going to have different functions for each different type of information we are going to extract using API calls
#1. Grab information about a summoner by summoner name by making an API call (and returns PUUID if needed in other functions)
def grabSummonerInfo(username):
#Making the API call to grab the information about the given username
    r = requests.get(api_SummonerURL+username+api_keyF)
#Saving the request into a JSON file
    summonerInfoJSON = json.loads(r.text)
#Formatting the saved text so I can write it to a file
    summonerInfoJSON_str = json.dumps(summonerInfoJSON, indent=2)
#Saving the summoner's details into an object of Summoner type
    summoner = Summoner()
    summoner.id = summonerInfoJSON['id']
    summoner.accountId = summonerInfoJSON['accountId']
    summoner.puuid = summonerInfoJSON['puuid']
    summoner.name = summonerInfoJSON['name']
    summoner.summonerLevel = summonerInfoJSON['summonerLevel']
#Printing the summoner's details
#MAKE SURE TO CHANGE WHEN USING OBJECTS IN OBJECTS TO PREVENT STACK OVERFLOW (use str method)
    print(vars(summoner))
#Test print to file; hardcoded -> change later
    with io.open(r'C:\Users\prefe\Documents\pitoane\LeagueMMDB\grabSummonerInfo.txt', "w", encoding='utf8') as outfile:
        outfile.write(summonerInfoJSON_str)
#Returns PUUID value when calling the function
    return summoner.puuid

#2. Grab a specific number of games from a specific date in the timeline
#Default values if not specified are grabbing last 10 games from today's date of ranked type (soloQ or flex) (and returns list with match IDs)
def grabSummonerGames(username, puuid=None, timeStart=None, timeEnd=None, queueType=None, queue=None, numberOfGames=None):
#Grab the given username's puuid
    puuid = grabSummonerInfo(username)
#If no end time is selected, set it to today's date
    if timeEnd==None:
        timeEnd=int(time.time())
#If no queue type is selected, set it to ranked (SoloQ & Flex)
    if queueType==None:
        queueType='ranked'
#If no queue selected, set it to SoloQ
    #if queue==None:
    #    queue=int(420)
#If no number of games is selected, set it to 10
    if numberOfGames==None:
        numberOfGames=10
#Set all parameters in one variable to be sent to the API call
    data={
        'endTime': timeEnd, 'type': queueType, 'count': numberOfGames, 'api_key': api_key
    }
#Send a request with the given params. to return matches ID
    r = requests.get(api_MatchURL+puuid+"/ids", params=data)
#Load given matches ID's into a JSON file for better formatting
    matchesJSON = json.loads(r.text)
#Formatting in order to write to file properly
    matchesJSON_str = json.dumps(matchesJSON, indent=2)
    matchesList = []
#Save all given matches into a list
    for match in matchesJSON:
        if match not in matchesList:
            matchesList.append(match)
#Print the values inside the list (the match IDs)
    print(*matchesList)
#Test print to file; hardcoded -> change later
    with io.open(r'C:\Users\prefe\Documents\pitoane\LeagueMMDB\grabSummonerGames.txt', "w", encoding='utf8') as outfile:
        outfile.write(matchesJSON_str)
#Returns match IDs when calling the function (as a list)
    return matchesList

#3. Grab info of a specific game
def grabGameInfo(matchID):
#Make a request to grab match details
    r = requests.get(api_SpecMatchURL+matchID+api_keyF)
#Saved grabbed match info into a JSON file
    gameInfoJSON = json.loads(r.text)
#Format the saved content into a string
    gameInfoJSON_str = json.dumps(gameInfoJSON, indent=2)
#Print the match info
    print(gameInfoJSON_str)
#Test print to file; hardcoded -> change later
    with io.open(r'C:\Users\prefe\Documents\pitoane\LeagueMMDB\grabGameInfo.txt', "w", encoding='utf8') as outfile:
        outfile.write(str(gameInfoJSON_str))

#4. Grab details about a specific game based on the given username
def grabGameSummonerInfo(username, matchID):
    pass

## test cases

#grabSummonerInfo('xKanelen')
#grabSummonerGames('xKanelen')
grabGameInfo('EUN1_3579371359')