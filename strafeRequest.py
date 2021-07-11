import json
import datetime
import time
import requests
import StakeDecisions
from config import *
from mysql_pool.mysqlhelper import MySqLHelper

# Start DB pool
db = MySqLHelper()


def strafeRequest(RequestType, RequestURL, **kwargs):
    strafeHeader = {
        "X-TimeZone": "-0700",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
        "User-Agent": "Strafe/2.40.8 (com.strafe.strafeapp; build:1233; iOS 14.6.0) Alamofire/4.9.1",
        "Accept-Language": "en-US,zh-Hans-US",
        "Authorization": "", # Needs to be filled
        "X-User-Agent": "iOS/2.40.8/1233",
    }

    # Send HTTP request
    if RequestType.lower() == "get":
        req = requests.get(RequestURL, headers=strafeHeader)
        # print("response code: ", req.status_code)
        # html = gzip.decompress(req.content) # Needs decode GZIP if using 'urllib.request' library
        html = req.content.decode("utf-8")  # UTF-8 Decode
        # print(html)
        return html
    elif RequestType.lower() == "post":
        # print("POST Requests")
        data = kwargs.get('data')
        # data = json.dumps(data)
        # print("data:", data)
        req = requests.post(RequestURL, headers=strafeHeader, json=data)
        # print("response code: ", req.status_code)
        # html = gzip.decompress(req.content) # GZIP decode with urllib.request
        html = req.content.decode("utf-8")  # UTF-8 Decode
        # print(html)
        return html
    else:
        return None


def getMatchData(matchID):
    matchPageURL = "https://flask-api.strafe.com/graphql/rest/matches/" + matchID + "/votes"
    matchPage = strafeRequest("get", matchPageURL)
    matchPageData = json.loads(matchPage)['data']
    return matchPageData


# voteChoice: string ("AWAY" or "HOME")
def castVote(matchID, voteChoice):
    castVoteURL = "https://flask-api.strafe.com/graphql/rest/matches/" + matchID + "/votes/cast"
    PostData = {"choice": voteChoice.upper()}
    if debugLevel >= 2:
        print(PostData)
    voteResult = strafeRequest("post", castVoteURL, data=PostData)
    if debugLevel >= 2:
        print(voteResult)
    return voteResult


# Main task
def taskQueue(strDate):
    calendarURL = "http://flask-api.strafe.com/v1.7/calendar/" + strDate
    calendarData = strafeRequest("get", calendarURL)
    calendarData = json.loads(calendarData)['data']  # convert string to json/dict
    print("Game Count: ", len(calendarData), "\n")  # Number of matches of the day
    # js = json.dumps(calendarData, sort_keys=True, indent=4, separators=(',', ':')) # Re-format for json
    # print(js, "\n")

    for i in range(len(calendarData)):
        # Cold down time
        time.sleep(3)

        teamTBD = False
        canVote = "NULL"
        print("[Match " + str(i + 1) + "/" + str(len(calendarData)) + "]")
        currentMatchDataData = calendarData[i]  # Load data
        print("Match uuid:", currentMatchDataData['uuid'])

        # MatchID
        matchID = currentMatchDataData['id']
        print("Match id:", matchID)

        # Match Time
        matchTime = currentMatchDataData['start_date']  # Format: 2013-07-12T07:00:00Z
        matchTime = datetime.datetime.strptime(matchTime, "%Y-%m-%dT%H:%M:%SZ")
        print("Match time (UTC): ", matchTime)

        # Event Name
        # Main event name
        currentEventName = currentMatchDataData['path'][0]['name']
        print("Event Name:", currentEventName)
        # Get all path ID and path name
        fullPathIDList = []
        fullPathName = ""
        for j in range(len(currentMatchDataData['path'])):
            fullPathIDList.append(currentMatchDataData['path'][j]['id'])
            fullPathName = fullPathName + " " + currentMatchDataData['path'][j]['name']
        print("Full path ID:", fullPathIDList)
        print("Full path name:", fullPathName)

        # Game Name
        GameType = currentMatchDataData['game']
        GameName = "Unknown"
        if GameType == 1:
            GameName = "CSGO"
            print("Game Name: CSGO")
        elif GameType == 2:
            GameName = "League of Legends"
            print("Game Name: League of Legends")
        elif GameType == 3:
            GameName = "DOTA2"
            print("Game Name: Dota2")
        elif GameType == 4:
            GameName = "SC2"
            print("Game Name: SC2")
        elif GameType == 5:
            GameName = "Hearthstone"
            print("Game Name: Hearthstone")
        elif GameType == 6:
            GameName = "Overwatch"
            print("Game Name: Overwatch")
        elif GameType == 7:
            GameName = "Rocket League"
            print("Game Name: Rocket League")
        elif GameType == 8:
            GameName = "R6"
            print("Game Name: Rainbow Six Siege")
        elif GameType == 9:
            GameName = "COD"
            print("Game Name: Call of Duty")
        elif GameType == 10:
            GameName = "Valorant"
            print("Game Name: Valorant")
        else:
            print("Game Name (Unknown): ", GameType)

        # Away Team
        try:
            AwayTeamName = currentMatchDataData['away']['name']
            AwayTeamID = currentMatchDataData['away']['id']
            print("Away team: ", currentMatchDataData['away']['name'])
            print("Away team ID:", AwayTeamID)
        except:
            teamTBD = True
            print("Away team: TBD")

        # Home Team
        try:
            HomeTeamName = currentMatchDataData['home']['name']
            HomeTeamID = currentMatchDataData['home']['id']
            print("Home team: ", HomeTeamName)
            print("Home team ID:", HomeTeamID)
        except:
            teamTBD = True
            print("Home team: TBD")

        # Match Status
        MatchStatus = currentMatchDataData['status']
        print("Match status:", MatchStatus)
        if not teamTBD:
            # Get each match data
            matchPageData = getMatchData(str(matchID))

            # Get match result
            if MatchStatus == "finished":
                try:
                    matchResult = matchPageData['result']
                except:
                    matchResult = "TBD"

            # Check Votable
            canVote = matchPageData['can_vote']
            print("can_vote:", canVote)
            if canVote == "NULL":
                print("Failed to get match vote status!")
            # elif canVote is False:
            # print("Match already voted!")
            else:
                try:
                    # L1 List: First list is home, the second is away [home, away, tie]
                    # L2 List: odds, votes_count [odds, votes_count]
                    # Tie selection always at 3rd spot
                    oddsData = [[0, 0], [0, 0], [0, 0]]

                    if matchPageData['available_choices'][0]['side'] == "home":
                        oddsData[0][0] = matchPageData['available_choices'][0]['odds']
                        oddsData[0][1] = matchPageData['available_choices'][0]['votes']
                        oddsData[1][0] = matchPageData['available_choices'][1]['odds']
                        oddsData[1][1] = matchPageData['available_choices'][1]['votes']
                    elif matchPageData['available_choices'][0]['side'] == "away":
                        oddsData[1][0] = matchPageData['available_choices'][0]['odds']
                        oddsData[1][1] = matchPageData['available_choices'][0]['votes']
                        oddsData[0][0] = matchPageData['available_choices'][1]['odds']
                        oddsData[0][1] = matchPageData['available_choices'][1]['votes']

                    try:
                        oddsData[2][0] = matchPageData['available_choices'][2]['odds']
                        oddsData[2][1] = matchPageData['available_choices'][2]['votes']
                    except:
                        print("The match result cannot be a tie")

                    print("-" * 20)
                    print("Home odds (" + HomeTeamName + "):", str(oddsData[0][0]) + ", Voted by", oddsData[0][1],
                          "people")
                    print("Away odds (" + AwayTeamName + "):", str(oddsData[1][0]) + ", Voted by", oddsData[1][1],
                          "people")
                except:
                    print("Error loading Odds/Rates")

            print("-" * 20)
            if debugLevel >= 2:
                print("oddsData List:", oddsData)
            VoteDecision = StakeDecisions.StakeDecisions([HomeTeamName, oddsData[0][0], oddsData[0][1]],
                                                         [AwayTeamName, oddsData[1][0], oddsData[1][1]])

            VoteDecisionTeam = "TBD"
            if autoVote:
                if MatchStatus.lower() == "upcoming" and canVote is True:
                    if AwayTeamName not in Blacklist_team:
                        if HomeTeamName not in Blacklist_team:
                            if currentEventName not in Blacklist_event:
                                if GameName not in Blacklist_game:
                                    if VoteDecision == 1 or VoteDecision == 3:
                                        VoteDecisionTeam = "HOME"
                                        voteResult = castVote(str(matchID), VoteDecisionTeam)
                                        print("Automatically stake on:", HomeTeamName)
                                    elif VoteDecision == 2 or VoteDecision == 4:
                                        VoteDecisionTeam = "AWAY"
                                        voteResult = castVote(str(matchID), VoteDecisionTeam)
                                        print("Automatically stake on:", AwayTeamName)
                                    else:
                                        print("Skipped the auto vote")
                                else:
                                    print("Current game is in the black list!")
                            else:
                                print("Current event is in the black list!")
                        else:
                            print("Home Team is in the black list!")
                    else:
                        print("Away Team is in the black list!")
                else:
                    print("The match is not votable!")
            else:
                print("Auto vote function is disabled")

            # Insert to DB
            currentTime = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            """ Start of SQL Write"""
            # Check if the match data already in DB (or if need to update)
            checkMatchStatusSql = "SELECT match_status FROM matches WHERE matchID = %s"
            try:
                dbResult = db.selectone(checkMatchStatusSql, param=str(matchID))[0].decode('utf-8')
            except:
                dbResult = None
            if debugLevel >= 2:
                print("DB check result:", dbResult)
            if dbResult is None:
                # New match record
                # Only insert if this is a new record
                # Only insert match info to DB when there's sufficient info (no TBD)
                if debugLevel >= 1:
                    print("Writing match data to DB!")
                # Table matches
                matchesTableSql = "INSERT INTO matches(matchID, start_time, away_teamID, away_team_name, home_teamID," \
                                  "home_team_name, game_type, pathID, event_name, full_path_name,match_status) " \
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                db.insertone(matchesTableSql, param=(str(matchID), str(matchTime), str(AwayTeamID), str(AwayTeamName),
                                                     str(HomeTeamID), str(HomeTeamName), str(GameType),
                                                     str(fullPathIDList),
                                                     str(currentEventName), str(fullPathName), str(MatchStatus)))
                # Table odds
                if debugLevel >= 2:
                    print("Current Time:", currentTime)
                oddsTableSql = "INSERT INTO odds(matchID, record_time, away_odds, home_odds, tie_odds, away_vote_count," \
                               "home_vote_count, tie_vote_count, stake_result, match_result)" \
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                db.insertone(oddsTableSql, param=(str(matchID), str(currentTime), str(oddsData[1][0]),
                                                  str(oddsData[0][0]), str(oddsData[2][0]), str(oddsData[1][1]),
                                                  str(oddsData[0][1]), str(oddsData[2][1]), str(VoteDecisionTeam),
                                                  str("TBD")))

            elif dbResult == "upcoming" and MatchStatus == "finished":
                # First time record the match is finished
                print("Match status changed! Updating DB record!")
                # Table matches (update match status)
                matchStatusChangeSql = "UPDATE matches SET match_status=finished WHERE matchID=%s"
                db.update(matchStatusChangeSql, param=str(matchID))

                # Table odds (add a record with final win result)
                oddsTableSql = "INSERT INTO odds(matchID, record_time, away_odds, home_odds, tie_odds, away_vote_count," \
                               "home_vote_count, tie_vote_count, stake_result, match_result)" \
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                db.insertone(oddsTableSql, param=(str(matchID), str(currentTime), str(oddsData[1][0]),
                                                  str(oddsData[0][0]), str(oddsData[2][0]), str(oddsData[1][1]),
                                                  str(oddsData[0][1]), str(oddsData[2][1]), str(VoteDecisionTeam),
                                                  str(matchResult)))
            elif dbResult == "upcoming" and MatchStatus == "upcoming":
                print("No update between current data and DB data! Only record odds data!")
            elif dbResult == "finished":
                print("DB Data locked for finished matches!")
                # Table odds
                currentTime = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                if debugLevel >= 2:
                    print("Current Time:", currentTime)
                oddsTableSql = "INSERT INTO odds(matchID, record_time, away_odds, home_odds, tie_odds, away_vote_count," \
                               "home_vote_count, tie_vote_count, stake_result, match_result)" \
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                db.insertone(oddsTableSql, param=(str(matchID), str(currentTime), str(oddsData[1][0]),
                                                  str(oddsData[0][0]), str(oddsData[2][0]), str(oddsData[1][1]),
                                                  str(oddsData[0][1]), str(oddsData[2][1]), str(VoteDecisionTeam),
                                                  str("TBD")))
            else:
                print("Unknown match status! No data written!")
            """End of SQL Write"""

        print("\n")
