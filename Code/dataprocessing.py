
'''
Programmet läser in en .csv-fil med all önskad data, inklusive odds.
Programmet skapar sedan en ny .csv-fil där samtliga matcher läggs in. 
Medelvärdet för de senaste 1, 3 och 5 mathcerna av viss matchstatistik för hemma- och bortalaget läggs även till för varje match.
Dessutom läggs variablerna som är givna på förhand, exempelvis matchodds, till. Efter denna process är datan processad färdig och kan användas för ML-syften.
.csv-filen sparas slutligen.
Programmet tar inte input. Användaren bes därmed att skriva in namnet på filen som läses in på rad 19, samt sitt önskade filnamn för den sparade filen på rad 132.
'''

import pandas as pd

# Statiska variabler väljs

static_variables = ['season','gameId','playerTeam','opposingTeam','gameDate', 'HomeOdds','DrawOdds','AwayOdds']

# Läser in datan och sorterar efter hemmalag, samt definierar det nya kalkylarket

df = pd.read_csv('cutDataWithOdds.csv') # Byt ut filnamnet om du så önskar
df_sorted = df.sort_values(['playerTeam', 'gameId'])
df_sorted = df_sorted.reset_index()
df_new = pd.DataFrame()

# Definierar de variablerna som ska användas

used_vars = ['faceOffsWonFor', 'hitsFor', 'takeawaysFor', 'giveawaysFor', 'faceOffsWonAgainst','hitsAgainst','takeawaysAgainst','giveawaysAgainst', 'shotAttemptsFor','goalsFor', 'shotAttemptsAgainst', 'goalsAgainst', 'shotsOnGoalFor', 'shotsOnGoalAway', 'xGoalsFor', 'xGoalsAgainst', 'penaltiesFor','penalityMinutesFor', 'penaltiesAgainst','penalityMinutesAgainst', 'Resultat']

# Loopar igenom de olika kolumnerna, och räknar ut dess historiska medelvärden för hemmalaget

home_team = df_sorted['playerTeam'][0]

for series_name, series in df_sorted.items():
    prevs = [[],[],[], []]
    counter = 0
    if series_name in static_variables:
        df_new.insert(0, series_name, series, True)
        continue
    if series_name not in used_vars:
        continue
    for index, row in df_sorted.iterrows(): 
        if row['playerTeam'] == home_team:
            if counter > 4:
                prevs[0].append(series[index-1])
                prevs[1].append((series[index-1]+series[index-2]+series[index-3])/3)
                prevs[2].append((series[index-1]+series[index-2]+series[index-3]+series[index-4]+series[index-5])/5)
                counter += 1
            elif counter > 2:
                prevs[0].append(series[index-1])
                prevs[1].append((series[index-1]+series[index-2]+series[index-3])/3)
                prevs[2].append(None)
                counter += 1
            elif counter > 0:
                prevs[0].append(series[index-1])
                prevs[1].append(None)
                prevs[2].append(None)
                counter += 1
            else:
                for i in range(3):
                    prevs[i].append(None)
                counter += 1
        else:
            counter = 0
            home_team = row['playerTeam']
            for i in range(3):
                prevs[i].append(None)
            counter += 1

    # Sparar medelvärdena i det nya kalkylarket

    for i in range(3):
        df_new.insert(0, series_name + "_home_" + str(i+1), prevs[i], True)

# Upprepar processen med historisk statistik för bortalaget

df_sorted = df_sorted.sort_values(['opposingTeam', 'gameId'])
df_sorted = df_sorted.reset_index()
df_new = df_new.sort_values(['opposingTeam', 'gameId'])
df_new = df_new.reset_index()

home_team = df_sorted['opposingTeam'][0]

for series_name, series in df_sorted.items():
    prevs = [[],[],[], []]
    counter = 0
    if series_name in static_variables:
        df_new.insert(0, series_name, series, True)
        continue
    if series_name not in used_vars:
        continue
    for index, row in df_sorted.iterrows(): 
        if row['opposingTeam'] == home_team:
            if counter > 4:
                prevs[0].append(series[index-1])
                prevs[1].append((series[index-1]+series[index-2]+series[index-3])/3)
                prevs[2].append((series[index-1]+series[index-2]+series[index-3]+series[index-4]+series[index-5])/5)
                counter += 1
            elif counter > 2:
                prevs[0].append(series[index-1])
                prevs[1].append((series[index-1]+series[index-2]+series[index-3])/3)
                prevs[2].append(None)
                counter += 1
            elif counter > 0:
                prevs[0].append(series[index-1])
                prevs[1].append(None)
                prevs[2].append(None)
                counter += 1
            else:
                for i in range(3):
                    prevs[i].append(None)
                counter += 1
        else:
            counter = 0
            home_team = row['opposingTeam']
            for i in range(3):
                prevs[i].append(None)
            counter += 1

    for i in range(3):
        df_new.insert(0, series_name + "_away_" + str(i+1), prevs[i], True)

# Hittar resultatet i matcherna och lägger till dessa

df_sorted.loc[df_sorted['iceTime'] != 3600, 'Resultat'] = 0.5

df_new.insert(0,'Resultat', df_sorted['Resultat'], True)
df_new = df_new[df_new.goalsFor_away_1.notnull()]

copy = df_new.copy()

copy['Resultat'] = copy['Resultat'].map({0: 'Loss', 1: 'Win', 0.5: 'Draw'})

copy.to_csv('processedData.csv', index=False) # Byt ut filnamnet om du så önskar

print("Program finished as expected.")
