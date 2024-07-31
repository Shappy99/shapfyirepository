# LeagueMH
 This is a script made in order to find out some interesting stats about your games based on your League of Legends match history.
 
 How it works?
 This script uses the Riot Games Developer API to make several calls in order to return different types of information from Riot (e.g. Game ID of games in match history and all stats of the games of your choice); then it formats the information and returns several interesting facts like: how many times have you met each player you've played with in the past; stats about the games or the encounters with each different player)
 !->to finish > upload info into a DB for easier data manipulation and add a config file for easier set-up; currently under work<-!
 
 How to use?
 -log in using the Riot Games Developer account into the Riot Developer Portal and grab your latest Riot API token
 -replace the Riot API Token with your working current key in the .env
 -call getSummonerInfo(inGameName) to receive info about your account
 -call getSummonerGames(inGameName, numberOfGames) to receive the Game ID of the desired number of games
 -call grabGameInfo(gameID, ...) to store all the data about the given games into different files for further processing/statistics
 -run LeagueMMDB\main.py
 -enjoy the data!