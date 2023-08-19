from bs4 import BeautifulSoup
import urllib
import math
import requests
from collections import defaultdict
import sys
from championInfo import getChamp

api_key = "RGAPI-10be0019-40b3-4b85-9293-c76c46a48470"
regionTranslate = {"NA":["na1", "americas"], "EUW":["euw1","europe"], "EUNE" : ["eun1", "europe"], "KR":["kr", "asia"],"OCE":["oc1","sea"]}


def InfoGet(userName,region, gameCount):
    # Get player Info
    r = regionTranslate[region][0]
    api_url_playerInfo = "https://"+r+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+userName + '?api_key=' + api_key

    req_playerInfo = requests.get(api_url_playerInfo)
    # print(req_playerInfo)
    player_info = req_playerInfo.json()
    #print(player_info)
    
    if "status" in player_info.keys():
        return "User Not Found"

    player_account_id = player_info["accountId"]
    player_name = player_info["name"]
    player_puuid = player_info["puuid"]
    player_lvl = player_info["summonerLevel"]


    # print(f"player name: {player_name} \nplayer level: {player_lvl} \npuuid: {player_puuid}")

    # Get matchId
    api_url_matchesId = "https://"+regionTranslate[region][1] +".api.riotgames.com/lol/match/v5/matches/by-puuid/"+player_puuid+"/ids?start=0&count="+str(gameCount)+"&api_key="+api_key
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
        api_url_matchInfo = "https://"+ regionTranslate[region][1]+".api.riotgames.com/lol/match/v5/matches/"+matchId+"?api_key="+api_key
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
    #print(commonBans)
    for k in commonBans.keys():
        if currGame >= maxGame:
            break
        print(f"    {k} : {commonBans[k]}", end="")
        currGame += 1
    print()
    
    winPercentage = recent_win / gameCount
    playerSummary = {"playerName" : player_name, 
                     "recentWin" : recent_win, 
                     "recentLose" : recent_lose, 
                     "streak" : streak, 
                     "winPercentage" : winPercentage, 
                     "winAgainst":win_against,
                     "loseAgainst" : lose_against,
                     "commonBans" : commonBans,
                     "matchHistory" : matchHistory,
                     "gameCount" : gameCount 
                     }

    playerSummary["comment"] = generateComment(playerSummary=playerSummary)
    return playerSummary

def generateComment(playerSummary):

    comment = ""
    
    comment = comment + playerSummary["playerName"] + " is doing"
    
    performance = [(0.25,"terrible","only"), (0.45, "poorly","only"), (0.50,"fine",""), (0.55, "well","a whopping amount of"), (1.00,"fantastic")]
    for i in range(len(performance)):
        #print(playerSummary["winPercentage"])
        if (playerSummary["winPercentage"] < performance[i][0]):
            comment = comment + " " + performance[i][1] + ". " + "Winning " + performance[i][2] + " " + str(playerSummary["recentWin" ]) + " out of his last " + str(playerSummary["gameCount"]) + " games and is on a" + " " + str(abs(playerSummary["streak"])) + " game"
            if (playerSummary["streak"] < 0):
                comment = comment + " lose streak."
            else:
                comment = comment + " win streak."
                
            comment = comment + " His greatest enemy is "
            
            for k in playerSummary["loseAgainst"].keys():
                comment = comment + k + " losing to it " + str(playerSummary["loseAgainst"][k]) + " times. So avoid talking about the strength of that champion."
                break
            
            for k in playerSummary["winAgainst"].keys():
                comment = comment + "He is doing well against " + k + " beating it " + str(playerSummary["winAgainst"][k]) + " times. "
                break
            break
    

    
    print(comment)
    return comment

x = InfoGet("Hide on bush","KR",10)
#print(x)
