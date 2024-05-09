import constants
import asyncio
import time
import re
import sqlite3
import csv
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
tourney_re = re.compile(r".*: \(.*\) vs \(.*\)")

async def main():
    cur = db.cursor()
    #cur.execute("CREATE TABLE games(id, match, users, events)")
    #name = await api.user("RMEfan", mode=GameMode.OSU, key=UserLookupKey.USERNAME)
    #print(name.id)
    #for i in range()
    # 110682497 rts gf
    # 107474593 ocl gf
    start_id = 107474593
    ids = (107474593, 110682497)
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
              107082999,107163395,107186478,107202847,107202335,107343096,107474593,)
    match = None
    overwrite = True

    if overwrite: 
        with open("csvfiles/testing.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(("Match ID", 
                        "Datetime", 
                        "Map ID", 
                        "User ID", 
                        "Username", 
                        "Mods", 
                        "Score"))
    for i in idsids:
        try:
            time.sleep(.2)
            match_response = await api.match(i)
        except ImportError:
            print()
            print(f"id {i} failed")
            continue
        #print()
        valid_match = re.fullmatch(tourney_re, match_response.match.name) != None
        #print(f"is '{match_response.match.name}' a tourney match? {valid_match}")
        if not valid_match: continue
        #print(match_response)
        users = match_response.users
        match = match_response.match
        fid = match_response.first_event_id
        lid = match_response.latest_event_id
        events = match_response.events
        
        #print(f"match id {i}")
        #print([user.username for user in users])
        user_dict = dict()
        for user in users:
            user_dict[user.id] = user.username
        #print(match)
        #print(f"first event id {fid}")
        #print(f"last event id  {lid}")

        
        lowest = 999999999999
        all_events = list()
        for event in events:
            lowest = min(lowest, event.id)
            all_events.append(event)
        while lowest > fid:
            new_match_response = aapi.match(i, before=lowest)
            more_events = new_match_response.events
            for event in more_events:
                if event.detail.type == MatchEventType.OTHER:
                    all_events.append(event)
                lowest = min(lowest, event.id)


        for event in all_events:
            lowest = min(lowest, event.id)
            #earliest = min(earliest, event.id)
            # print(f"id {event.id}")
            if not event.detail.type == MatchEventType.OTHER:
                # print("hey")
                continue
            game = event.game
            eid = event.id
            etime = event.timestamp
            teamtype = event.game.team_type
            bm = game.beatmap
            if not bm: continue
            bm_id = game.beatmap_id
            mset = bm._beatmapset
            #print(f"\nevent id {eid} played {mset.artist} - {mset.title}")
            for score in game.scores:
                #print(f"{user_dict[score.user_id]} got {score.score} on {bm_id}")
                line = (i, 
                        etime, 
                        bm_id, 
                        score.user_id, 
                        user_dict[score.user_id], 
                        score.mods, 
                        score.score)
                await write_csv(line)
    pass


async def write_csv(obj):
    # TODO: use append mode for multiple sessions
    with open("csvfiles/testing.csv", "a", newline='') as f:

        writer = csv.writer(f)
        writer.writerow(obj)
        

asyncio.run(main())