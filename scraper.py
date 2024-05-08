import constants
import asyncio
import time
import re
import sqlite3
import csv
from time import sleep
from constants import *
from ossapi import OssapiAsync, UserLookupKey, GameMode, RankingType, MatchEventType, BeatmapsetCompact


api = OssapiAsync(CLIENT_ID, API_KEY)
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
    start_id = 107474593
    match = None
    for i in range(start_id, start_id + 1):
        try:
            time.sleep(.1)
            match_response = await api.match(i)
        except Exception:
            print(f"id {i} failed")
            continue
        print()
        valid_match = re.fullmatch(tourney_re, match_response.match.name) != None
        print(f"is '{match_response.match.name}' a tourney match? {valid_match}")
        if not valid_match: continue

        users = match_response.users
        match = match_response.match
        fid = match_response.first_event_id
        lid = match_response.latest_event_id
        events = match_response.events
        
        print(f"id {i}")
        print([user.username for user in users])
        user_dict = dict()
        for user in users:
            user_dict[user.id] = user.username
        print(match)
        print(fid)
        print(lid)
        for event in events:
            # print(f"id {event.id}")
            if not event.detail.type == MatchEventType.OTHER:
                # print("hey")
                continue
            game = event.game
            eid = event.id
            etime = event.timestamp
            teamtype = event.game.team_type
            bm = game.beatmap
            bm_id = game.beatmap_id
            mset = bm._beatmapset
            print(f"played {mset.artist} - {mset.title}")
            for score in game.scores:
                print(f"{user_dict[score.user_id]} got {score.score} on {bm_id}")
                line = (i, 
                        match.end_time, 
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