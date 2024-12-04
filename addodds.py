
'''
Programmet läser in två .csv-filer, en med fullständig matchstatistik och en med odds till varje match.
Matcherna från varje dataset paras ihop, och en ny .csv-fil med både matchstatistik och odds skapas och sparas.
Här tas även vissa meningslösa kolumner från matchstatistiken bort.
Programmet tar inte input. Användaren bes därmed skriva in namnet på filen med matchstatistik på rad 13 samt filen med odds på rad 14, och dess önskade namn på filen som ska sparas på rad 51.
'''

import pandas as pd

# Läser in de två .csv-filerna

df_odds = pd.read_csv("exampleData.csv") # Byt ut filnamnet om du så önskar
df_large = pd.read_csv("exampleOdds.csv") # Byt ut filnamnet om du så önskar

# Sätter ihop dataseten

df_merged = pd.merge(
    df_large,
    df_odds,
    left_on=['gameDate', 'opposingTeam'],
    right_on=['Date', 'Away Team'],
    how='left'
)

# Byter namn på vissa kolumner

df_merged.rename(columns={
    'Home Odds': 'HomeOdds',
    'Draw Odds': 'DrawOdds',
    'Away Odds': 'AwayOdds'
}, inplace=True)

# Väljer relevanta kolumner

df_large = df_merged[df_large.columns.tolist() + ['HomeOdds', 'DrawOdds', 'AwayOdds']]

df_large = df_large[df_large.HomeOdds.notnull()]
df_large = df_large[df_large.playoffGame == 0]

# Tar bort meningslösa kolumner

df_large = df_large.drop('position', axis=1)
df_large = df_large.drop('situation', axis=1)
df_large = df_large.drop('team', axis=1)
df_large = df_large.drop('name', axis=1)
df_large = df_large.drop('playoffGame', axis=1)
df_large = df_large.drop('home_or_away', axis=1)

# Sparar den nya .csv-filen

df_large.to_csv("exampleDataWithOdds", index=False) # Byt ut filnamnet om du så önskar

print("Program finished as expected.")
