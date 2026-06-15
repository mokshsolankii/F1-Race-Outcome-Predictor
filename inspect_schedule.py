import fastf1
import pandas as pd

# Load schedule for 2023
schedule = fastf1.get_event_schedule(2023)
print("Columns:", schedule.columns.tolist())
print(schedule[['RoundNumber', 'EventName', 'EventFormat']].head())
