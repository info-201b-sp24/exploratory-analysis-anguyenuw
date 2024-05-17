import constants
import asyncio
import time
import re
import sqlite3
import csv
import datetime
import traceback
from time import sleep
from constants import *
from ossapi import OssapiAsync, UserLookupKey, GameMode, RankingType, MatchEventType, BeatmapsetCompact, Ossapi


api = OssapiAsync(CLIENT_ID, API_KEY)
aapi = Ossapi(CLIENT_ID, API_KEY)
db = sqlite3.connect("awesome.db")

#print(api.user(12092800, mode="osu").username)
#print(api.beatmap(221777).id)

# a tournament match is defined as a multiplayer match whose name fits the format
#   ABBR: (team 1) vs (team 2)
tourney_re = re.compile(r".*: \(.*\) [vV][sS]?\.? \(.*\)")

async def scrape_known_mps():
    cur = db.cursor()
    #cur.execute("CREATE TABLE games(id, match, users, events)")
    #name = await api.user("RMEfan", mode=GameMode.OSU, key=UserLookupKey.USERNAME)
    #print(name.id)
    #for i in range()
    # 110682497 rts gf
    # 107474593 ocl gf
    start_id = 107474593
    ids = (107474593, 110682497)
    # all ocl bracket w23
    idsids = (106688657,106688649,106684920,106647595,
              106669944,106682522,106684444,106643259,
              106686882,106687250,106691174,106670157,
              106658486,106689954,106656606,106687881,
              106794631,106776842,106815981,106790536,
              106799336,106800874,106777737,106793462,
              106786766,106818363,106798741,106852090,
              106803191,106820877,106812248,106904898,
              106917336,106923782,106918548,106923863,
              106916011,106886444,106940816,106928547,
              106958795,106929508,106938605,106967008,
              106944371,106925641,107064293,107056176,
              107053416,107058578,107066561,107078386,
              107082999,107163395,107186478,107202847,107202335,107343096,107474593)
    # ocl qual w23
    moreidsids = (106503364, 106508352, 106526178, 106526896, 106528049, 106530354, 106534327, 106531363, 106540332, 106541457, 106545033, 106549892, 106551091, 106553123, 106554423, 106555769)
    ads_24_d1 = (113104530,113122523,113123198,112996405,113006237,113026360,113027534,112832449,112927390,112912565,112925753,112927374,112928548,112930240,112929414,112831314,112929834,112800830,112913789)
    owc_23 = (111534249,111554331,111555364,111451190,111457054,111460173,111466879,111349795,111350765,111352735,111356742,111360796,111366414,111368903,111372515,111253985,111256134,111256976,111257938,111258934,111260018,111260487,111261974,111265019,111271525,111272312,111273436,111273441,111274743,111276018,111278789,111152642,111165133,111167951,111168903,111170809,111170821,111171785,111178942,111178945,111183369,111183363,111183770,111184163,111184941,111187488,111188366,111062319,111063878,111072298,111073334,111073335,111081251,111083508,111083501,111084580,111085330,111085320,111085343,111086282,111086205,111087337,111091065)
    match = None
    overwrite = True
    dest = "csvfiles/garbage.csv"
    #logdest = "csvfiles/id_abbreviations.csv"
    if overwrite: 
        with open(dest, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(("Match ID", 
                        "Datetime", 
                        "Map ID", 
                        "User ID", 
                        "Username", 
                        "Mods", 
                        "Score"))
    for i in owc_23:
        try:
            match_response = await api.match(i)
        except Exception:
            print(f"id {i} failed")
            continue
        #print()
        valid_match = re.fullmatch(tourney_re, match_response.match.name) != None
        print(f"is '{match_response.match.name}' a tourney match? {valid_match}")
        if not valid_match: continue
        #print(match_response)
        abbr = (match_response.match.name[0:match_response.match.name.find(":")]).strip()
        #await write_csv((abbr, i), logdest)
        users = match_response.users
        match = match_response.match
        fid = match_response.first_event_id
        lid = match_response.latest_event_id
        events = match_response.events
        print(f"match id {i}")
        #print([user.username for user in users])
        user_dict = dict()
        for user in users:
            user_dict[user.id] = user.username
        #print(match)
        #print(f"first event id {fid}")
        #print(f"last event id  {lid}")

        # gather all of the maps played in this match
        lowest = 999999999999
        all_events = list()
        for event in events:
            lowest = min(lowest, event.id)
            if event.detail.type == MatchEventType.OTHER:
                all_events.append(event)
        while lowest > fid:
            new_match_response = aapi.match(i, before=lowest)
            for user in new_match_response.users:
                user_dict[user.id] = user.username
            more_events = new_match_response.events
            for event in more_events:
                if event.detail.type == MatchEventType.OTHER:
                    all_events.append(event)
                lowest = min(lowest, event.id)

        # skip if no maps were played
        if not all_events: continue

        # first pass - find the most common amount of players per map
        playercounts = dict()
        for event in all_events:
            if not event.detail.type == MatchEventType.OTHER: continue
            num_players = len(event.game.scores)
            if num_players not in playercounts:
                playercounts[num_players] = 0
            playercounts[num_players] += 1
            #print(playercounts)
        
        most_common_player_count = max(playercounts, key=playercounts.get)
        print(f"most common: {most_common_player_count}")
            

        # second pass - for each map, for each score, write a csv row about that score 
        #     skip any maps with unusual player counts
        for event in all_events:
            # if not event.detail.type == MatchEventType.OTHER:
            #     # print("hey")
            #     continue
            game = event.game
            eid = event.id
            etime = event.timestamp
            teamtype = event.game.team_type
            bm = game.beatmap
            if not bm: continue
            bm_id = game.beatmap_id
            mset = bm._beatmapset
            #print(f"\nevent id {eid} played {mset.artist} - {mset.title}")
            if not len(game.scores) == most_common_player_count: continue
            for score in game.scores:
                #print(f"{user_dict[score.user_id]} got {score.score} on {bm_id}")
                line = (i, 
                        etime, 
                        bm_id, 
                        score.user_id, 
                        user_dict[score.user_id], 
                        score.mods, 
                        score.score)
                await write_csv(line, dest)
    pass

async def scrape_all():
    # range history
    # 106002000, 106026500, 106051000, 106075500, 106090600
    # 106090600, 106470600, 106850600, 107230600, 107610600, 107978000
    # 108317000, 108655500, 108994000, 109332500, 109671000, 110000000
    # crashed, need to start from borders
    #       108495608, 108834130, 109171244, 109510534, 109848136
    start_id = 109848136
    end_id =   110000000
    overwrite = False
    dest = "csvfiles/all_mps.csv"
    logdest = "csvfiles/id_abbrs.csv"
    # if overwrite: 
    #     with open(dest, "w", newline='') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(("Match ID", 
    #                     "Tourney Abbreviation",
    #                     "Datetime", 
    #                     "Map ID", 
    #                     "User ID", 
    #                     "Username", 
    #                     "Mods", 
    #                     "Score"))
    prev_time = datetime.datetime.now()
    for i in range(start_id, end_id):
        try:
            #time.sleep(.08)
            match_response = await api.match(i)
        except Exception:
            if (i%100 == 0): 
                time = datetime.datetime.now()
                print(f"id {i} fail : 100 took {time - prev_time}")
                prev_time = time

            continue
        try:
            valid_match = re.fullmatch(tourney_re, match_response.match.name) != None
            if not valid_match: continue
            
            abbr = (match_response.match.name[0:match_response.match.name.find(":")]).strip()
            await write_csv((abbr, i), logdest)
            users = match_response.users
            fid = match_response.first_event_id
            events = match_response.events
            if (i%20 == 0): print(f"match id {i} success")
            user_dict = dict()
            for user in users:
                user_dict[user.id] = user.username

            # gather all of the maps played in this match
            lowest = 999999999999
            all_events = list()
            for event in events:
                lowest = min(lowest, event.id)
                if event.detail.type == MatchEventType.OTHER:
                    all_events.append(event)
            while lowest > fid:
                new_match_response = aapi.match(i, before=lowest)
                for user in new_match_response.users:
                    user_dict[user.id] = user.username
                more_events = new_match_response.events
                for event in more_events:
                    if event.detail.type == MatchEventType.OTHER:
                        all_events.append(event)
                    lowest = min(lowest, event.id)

            # skip if no maps were played
            if not all_events: continue

            # first pass - find the most common amount of players per map
            playercounts = dict()
            for event in all_events:
                if not event.detail.type == MatchEventType.OTHER: continue
                num_players = len(event.game.scores)
                if num_players not in playercounts:
                    playercounts[num_players] = 0
                playercounts[num_players] += 1
                #print(playercounts)
            
            most_common_player_count = max(playercounts, key=playercounts.get)
            #print(f"most common: {most_common_player_count}")
                

            # second pass - for each map, for each score, write a csv row about that score 
            #     skip any maps with unusual player counts
            for event in all_events:
                game = event.game
                etime = event.timestamp
                bm = game.beatmap
                if not bm: continue
                bm_id = game.beatmap_id
                if not len(game.scores) == most_common_player_count: continue
                for score in game.scores:
                    line = (i, 
                            abbr, 
                            etime, 
                            bm_id, 
                            score.user_id, 
                            user_dict[score.user_id], 
                            score.mods, 
                            score.score)
                    await write_csv(line, dest)
        except Exception:
            with open("errorlog.txt", "a", newline='', encoding='utf-8') as f:
                print(f"something went wrong id {i}", file=f)
                print("\nERROR: \n", file=f)
                traceback.print_exc(file=f)
        

async def test():
    idsids = (106688657,106688649,106684920,106647595,
              106669944,106682522,106684444,106643259,
              106686882,106687250,106691174,106670157,
              106658486,106689954,106656606,106687881,
              106794631,106776842,106815981,106790536,
              106799336,106800874,106777737,106793462,
              106786766,106818363,106798741,106852090,
              106803191,106820877,106812248,106904898,
              106917336,106923782,106918548,106923863,
              106916011,106886444,106940816,106928547,
              106958795,106929508,106938605,106967008,
              106944371,106925641,107064293,107056176,
              107053416,107058578,107066561,107078386,
              107082999,107163395,107186478,107202847,107202335,107343096,107474593)
    
    with open('known_IDs.txt','w') as f:
        f.write(str({1,3,(3,5)}))  # set of numbers & a tuple



async def write_csv(obj, filename):
    # TODO: use append mode for multiple sessions
    with open(filename, "a", newline='', encoding='utf-8') as f:

        writer = csv.writer(f)
        writer.writerow(obj)
        

asyncio.run(scrape_all())