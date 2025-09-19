#!/usr/bin/env python3
import os, time, datetime
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

# — CONFIG — 
INPUT_CSV    = '/Users/abhik/Desktop/info2015.csv'
OUTPUT_CSV   = '/Users/abhik/Desktop/info2015_with_yoe.csv'
DELAY        = 0.6   # seconds between API calls to avoid throttling
TARGET_YEAR  = 2015  # change this if you want a past/future season

# — VERIFY INPUT — 
if not os.path.isfile(INPUT_CSV):
    raise FileNotFoundError(f"Could not find input CSV at {INPUT_CSV!r}")

# — LOAD PLAYERS — 
df = pd.read_csv(INPUT_CSV)
yoe_list = []

# — MAIN LOOP — 
for full_name in df['Player']:
    yoe = None
    try:
        # 1) Find player ID
        matches = players.find_players_by_full_name(full_name)
        if matches:
            pid = matches[0]['id']
            # 2) Fetch career stats
            career = playercareerstats.PlayerCareerStats(player_id=pid)
            df_career = career.get_data_frames()[0]
            # 3) Determine rookie year from first SEASON_ID (e.g. "2018-19")
            rookie_season = df_career.loc[0, 'SEASON_ID']
            rookie_year = int(rookie_season.split('-')[0])
            # 4) Compute YOE
            yoe = TARGET_YEAR - rookie_year + 1
    except Exception:
        yoe = None

    yoe_list.append(yoe)
    print(f"{full_name:30s} → YOE up to {TARGET_YEAR}: {yoe or '0'}")
    time.sleep(DELAY)

# — SAVE RESULTS — 
df['YOE'] = yoe_list
df.to_csv(OUTPUT_CSV, index=False)
print(f"\nDone! Wrote {len(df)} players with YOE to:\n  {OUTPUT_CSV}")
