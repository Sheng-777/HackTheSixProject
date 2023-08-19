from bs4 import BeautifulSoup
import urllib
import math
import requests
from collections import defaultdict
import sys
from championInfo import getChamp

api_key = "RGAPI-10be0019-40b3-4b85-9293-c76c46a48470"
regionTranslate = {"NA":"na1", "EUW":"euw1", "EUNE" : "eun1", "KR":"kr","OCE":"oc1"}


def InfoGet(userName,region, gameCount):
    # Get player Info
    region = regionTranslate[region]
    api_url_playerInfo = "https://"+region+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+userName + '?api_key=' + api_key

    req_playerInfo = requests.get(api_url_playerInfo)
    # print(req_playerInfo)
    player_info = req_playerInfo.json()
    #print(player_info)
    
    if player_info["status"]["status_code"] == 404:
        return "User Not Found"

    player_account_id = player_info["accountId"]
    player_name = player_info["name"]
    player_puuid = player_info["puuid"]
    player_lvl = player_info["summonerLevel"]


    # print(f"player name: {player_name} \nplayer level: {player_lvl} \npuuid: {player_puuid}")

    # Get matchId
    api_url_matchesId = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+player_puuid+"/ids?start=0&count="+str(gameCount)+"&api_key="+api_key
    req_matchesId = requests.get(api_url_matchesId)
    matches_id = req_matchesId.json()
    # print(matches_id)

    # get matches info
    recent_win = 0
    recent_lose = 0
    streak = 0
    on_streak = True
    win_against = defaultdict(int)
    lose_against = defaultdict(int)
    avgKDA = 0
    avgCSperMin = 0
    commonBans = defaultdict(int)
    winPercentage = 0

    matchHistory = []
    
    #iterate over each math
    for matchId in matches_id:
        api_url_matchInfo = "https://americas.api.riotgames.com/lol/match/v5/matches/"+matchId+"?api_key="+api_key
        req_matchInfo = requests.get(api_url_matchInfo)
        matchInfo = req_matchInfo.json()
        #print(matchInfo["info"]["teams"][9//5]["bans"][9 % 5])
        #sys.exit()
        matchDetail = []
        
        participants = matchInfo["info"]["participants"]
        #print(participants)
        teams = ["Red","Blue"]
        winTeam = teams[int(participants[0]["win"])]
        matchDetail.append(winTeam)
        print("Winner: " + winTeam)
        for i in range(len(participants)):
            
            if (i == 0):
                print("Team Blue:")
            elif (i == 5):
                print("Team Red:")
            
            #print(participants[i])
            #break
            
            summonerName = participants[i]["summonerName"]
            champion = participants[i]["championName"]
            kills = participants[i]["kills"]
            deaths = participants[i]["deaths"]
            assists = participants[i]["assists"]
            win = participants[i]["win"]
            csPerMinute = round((participants[i]["totalMinionsKilled"] + participants[i]["neutralMinionsKilled"]) / ((participants[i]["timePlayed"] / 60)), 1)
            
            matchDetail.append([summonerName,champion,kills,deaths,assists,csPerMinute])
            
            
            if summonerName == player_name:
                if win:
                    recent_win += 1
                    if on_streak:
                        if streak >= 0:
                            streak += 1
                        else:
                            on_streak = False
                    
                    if (i < 5):
                        for j in range(5,len(participants)):
                            win_against[participants[j]["championName"]] += 1
                    else:
                        for j in range(5):
                            win_against[participants[j]["championName"]] += 1
                        
                        
                else:
                    recent_lose += 1
                    if on_streak:
                        if streak <= 0:
                            streak -=1
                        else:
                            on_streak = False
                    
                    if (i < 5):
                        for j in range(5,len(participants)):
                            lose_against[participants[j]["championName"]] += 1
                    else:
                        for j in range(5):
                            lose_against[participants[j]["championName"]] += 1
                 
                try:       
                    commonBans[getChamp(matchInfo["info"]["teams"][i//5]["bans"][i % 5]["championId"])] += 1
                except:
                    pass
            print(f"    summoner name: {summonerName} | champions: {champion} | kills: {kills} | deaths: {deaths} | assists: {assists} | cs/m: {csPerMinute}| win: {win}")
        
        
        #break
        matchHistory.append(matchDetail)
        print("--------------------------------")

    print(f"{userName} Summary:")

    print(f"recent streak: {streak}")
    print(f"recent win: {recent_win}")
    print(f"recent lose: {recent_lose}")
    

    print("Top 3 Win against:")
    maxGame = 3
    currGame = 0

    win_against = {k:v for k, v in reversed(sorted(win_against.items(),key=lambda item: item[1]))}
    for k in win_against.keys():
        if currGame >= maxGame:
            break 
        print(f"    {k} : {win_against[k]}", end="")
        currGame += 1
    print()    

    print("Top 3 lose against:")
    currGame = 0
    lose_against = {k:v for k, v in reversed(sorted(lose_against.items(),key=lambda item: item[1]))}
    for k in lose_against.keys():
        if currGame >= maxGame:
            break
        print(f"    {k} : {lose_against[k]}", end="")
        currGame += 1
    print()
    
    print("Top Bans")
    currGame = 0
    commonBans = {k:v for k, v in reversed(sorted(commonBans.items(),key=lambda item: item[1]))}
    print(commonBans)
    for k in commonBans.keys():
        if currGame >= maxGame:
            break
        print(f"    {k} : {commonBans[k]}", end="")
        currGame += 1
    print()
    
    winPercentage = recent_win / gameCount
    playerSummary = [player_name,recent_win,recent_lose,streak,winPercentage,win_against,lose_against,commonBans,matchHistory]
    
    return playerSummary

x = InfoGet("_ - ","NA",10)
print(x)