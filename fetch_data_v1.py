import fastf1
import pandas as pd
import os

# Create cache directory
os.makedirs('f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('f1_cache')

years = [2021, 2022, 2023, 2024, 2025, 2026]
all_records = []

for year in years:
    print(f"\n=================== Year: {year} ===================")
    try:
        schedule = fastf1.get_event_schedule(year)
    except Exception as e:
        print(f"Error fetching schedule for {year}: {e}")
        continue
        
    for _, event in schedule.iterrows():
        # Skip testing
        if event['EventFormat'] == 'testing':
            continue
            
        round_num = event['RoundNumber']
        if round_num <= 0:
            continue
            
        race_name = event['EventName']
        print(f"Loading {year} Round {round_num}: {race_name}...")
        
        try:
            # Fetch the race session
            race = fastf1.get_session(year, round_num, 'R')
            # Load only the results (no telemetry, weather, or laps to make it fast)
            race.load(laps=False, telemetry=False, weather=False)
            
            # Check results
            if race.results is None or len(race.results) == 0:
                print(f"No results for {year} {race_name} (session might not have occurred yet).")
                continue
                
            count = 0
            for _, row in race.results.iterrows():
                driver = row['Abbreviation']
                team = row['TeamName']
                grid = row['GridPosition']
                position = row['Position']
                
                # Basic validation
                if pd.isna(position) or pd.isna(grid) or not driver or not team:
                    continue
                    
                all_records.append({
                    'season': year,
                    'circuit': race_name,
                    'driver': driver,
                    'team': team,
                    'grid_position': int(grid),
                    'finish_position': int(position)
                })
                count += 1
            print(f"Successfully loaded {count} drivers for {year} {race_name}")
            
        except Exception as e:
            print(f"Skipping {year} {race_name} due to error: {e}")

# Save to CSV
df = pd.DataFrame(all_records)
output_path = 'f1_v1_data.csv'
df.to_csv(output_path, index=False)
print(f"\n=================== Process Complete ===================")
print(f"Collected a total of {len(df)} records.")
print(f"Saved dataset to {output_path}")
print(df.head())
