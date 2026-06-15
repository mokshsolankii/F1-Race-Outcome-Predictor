import fastf1
session = fastf1.get_session(2023, 'Bahrain', 'R')
session.load(laps=False, telemetry=False, weather=False)
print("Results Columns:", session.results.columns.tolist())
print(session.results[['Abbreviation', 'TeamName', 'Grid', 'Position']].head())
