from bs4 import BeautifulSoup
import urllib
import requests


api_key = "RGAPI-e1e8622d-c3d8-4599-80d4-9a9e842416e3"
userName = "Sheng777"

# Get player Info
api_url_playerInfo = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+userName + '?api_key=' + api_key

req_playerInfo = requests.get(api_url_playerInfo)
# print(req_playerInfo)
player_info = req_playerInfo.json()
# print(player_info)

player_account_id = player_info["accountId"]
player_name = player_info["name"]
player_puuid = player_info["puuid"]
player_lvl = player_info["summonerLevel"]


# print(f"player name: {player_name} \nplayer level: {player_lvl} \npuuid: {player_puuid}")

# Get matchId
api_url_matchesId = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+player_puuid+"/ids?start=0&count=20"+"&api_key="+api_key
req_matchesId = requests.get(api_url_matchesId)
matches_id = req_matchesId.json()
# print(matches_id)

# get detail match info
recent_win = 0
recent_lose = 0
streak = 0
on_streak = True

for matchId in matches_id:
    api_url_matchInfo = "https://americas.api.riotgames.com/lol/match/v5/matches/"+matchId+"?api_key="+api_key
    req_matchInfo = requests.get(api_url_matchInfo)
    matchInfo = req_matchInfo.json()
    #print(matchInfo["info"]["teams"][0])
    #print(matchInfo["info"]["teams"][0])

    participants = matchInfo["info"]["participants"]
    #print(participants)
    
    
    for i in range(len(participants)):
        #break    
        summonerName = participants[i]["summonerName"]
        champion = participants[i]["championName"]
        kills = participants[i]["kills"]
        deaths = participants[i]["deaths"]
        assists = participants[i]["assists"]
        win = participants[i]["win"]        
        
        if summonerName == player_name:
            if win:
                recent_win += 1
                if on_streak:
                    if streak >= 0:
                        streak += 1
                    else:
                        on_streak = False
                    
                    
            else:
                recent_lose += 1
                if on_streak:
                    if streak <= 0:
                        streak -=1
                    else:
                        on_streak = False
        
        print(f"    summoner name: {summonerName} | champions: {champion} | kills: {kills} | deaths: {deaths} | assists: {assists} | win: {win}")
    
    
    #break
    print("--------------------------------")

print("Summary:")

print(f"recent streak: {streak}")
print(f"recent win: {recent_win}")
print(f"recent lose: {recent_lose}")
