# Do NOT use it in real stakes
def StakeDecisions(HomeData, AwayData):
    # returnDecision = 1 -- > Vote for Home
    # returnDecision = 2 -- > Vote for Away
    # returnDecision = 3 -- > Prefer Home
    # returnDecision = 4 -- > Prefer Away
    # returnDecision = 5 -- > Cannot Decide
    returnDecision = 5

    # Read Black List (will not vote teams in this list)
    blackList = []
    for line in open("config.py"):
        blackList.append(line)

    # Read Data
    HomeTeamName = HomeData[0]
    AwayTeamName = AwayData[0]
    HomeOdds = HomeData[1]
    CurrentHomeVotes = HomeData[2]
    AwayOdds = AwayData[1]
    CurrentAwayVotes = AwayData[2]
    # print("Home: ", HomeTeamName, ", Odds:", HomeOdds, ", Votes:", CurrentHomeVotes)
    # print("Away: ", AwayTeamName, ", Odds:", AwayOdds, ", Votes:", CurrentAwayVotes)

    if CurrentHomeVotes == 0:
        CurrentHomeVotes = 1
    if CurrentAwayVotes == 0:
        CurrentAwayVotes = 1

    # Avoid Black List Team
    if HomeTeamName in blackList:
        returnDecision = 5
        print(HomeTeamName, "is in black list!")
    elif AwayTeamName in blackList:
        returnDecision = 5
        print(AwayTeamName, "is in black list!")
    else:
        try:
            oddsDivision = HomeOdds / AwayOdds
            if oddsDivision == 1:
                # Same Odds
                print("Need human's decision")

                # Decided by division of current votes number
                if (CurrentHomeVotes / CurrentAwayVotes) >= 5 or (CurrentHomeVotes - CurrentAwayVotes) >= 25:
                    returnDecision = 1
                if (CurrentAwayVotes / CurrentHomeVotes) >= 5 or (CurrentAwayVotes - CurrentHomeVotes) >= 25:
                    returnDecision = 2
            elif oddsDivision > 1:
                print("Odds Division:", oddsDivision)
                print("Away Team is leading in odds")

                # Decided by Odds Division
                if oddsDivision >= 2.5:
                    returnDecision = 2
                    print("Voted because of high odds division")
                else:
                    # Decided by division of current votes number
                    if (CurrentHomeVotes / CurrentAwayVotes) >= 3.1:
                        print("Community strongly believes in Away Team!")
                        returnDecision = 1
                    elif CurrentAwayVotes / CurrentHomeVotes >= 1.25:
                        returnDecision = 2
                        print("Voted because of normal odds division and community's choices")
                    elif CurrentAwayVotes - CurrentHomeVotes >= 50:
                        returnDecision = 2
                        print("Voted because of normal odds division and community's choices")
                    elif (CurrentHomeVotes / CurrentAwayVotes) >= 1.75:
                        print("Need human double check!")
                        returnDecision = 3
                    else:
                        print("Unknown situation")
                        returnDecision = 5
            else:
                oddsDivision = 1 / oddsDivision
                print("Odds Division:", oddsDivision)
                print("Home Team is leading in odds")

                # Decided by Odds Division
                if oddsDivision >= 2.5:
                    returnDecision = 1
                else:
                    # Decided by division of current votes number
                    if (CurrentAwayVotes / CurrentHomeVotes) >= 3.1:
                        print("Community strongly believes in Away Team!")
                        returnDecision = 2
                    elif (CurrentHomeVotes / CurrentAwayVotes) >= 1.25:
                        returnDecision = 1
                        print("Voted because of normal odds division and community's choices")
                    elif CurrentHomeVotes - CurrentAwayVotes >= 50:
                        returnDecision = 1
                        print("Voted because of normal odds division and community's choices")
                    elif (CurrentAwayVotes / CurrentHomeVotes) >= 1.75:
                        print("Need human double check!")
                        returnDecision = 4
                    else:
                        print("Unknown situation")
                        returnDecision = 5
        except:
            print("Unknown Error! Maybe caused by NULL data")
            returnDecision = 5

    return returnDecision
