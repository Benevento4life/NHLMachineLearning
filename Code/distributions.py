
'''
Programmet läser in ett antal .csv-filer med förutsägningar i några simuleringar.
Därefter skriver programmet ut medelvärde och standardavvikelse i fördelningen av slumpad betting på dessa matcher i varje simulering, som beskrivit i metoden.
Programmet tar inte input. Istället bes användaren att skriva in namnet på filen i raderna 57-67.
'''

import pandas as pd

# Se bettingsimulation.py för förklaring av denna funktion

def find_balance(df):

    balance1 = 10000
    balances = [10000]

    games = []

    for index, row in df.iterrows():
        home_prob = (1/float(row['HomeOdds']))
        away_prob = (1/float(row['AwayOdds']))
        draw_prob = (1/float(row['DrawOdds']))
        if row['prediction_label'] == 'Win':
            if row['prediction_score'] > home_prob:
                games.append(True)
                if row['Resultat'] == 'Win':
                    balance1 += (100/home_prob -100)
                else:
                    balance1 -= 100
            else:
                games.append(False)
        elif row['prediction_label'] == 'Loss':
            if row['prediction_score'] > away_prob:
                games.append(True)
                if row['Resultat'] == 'Loss':
                    balance1 += (100/away_prob -100)
                else:
                    balance1 -= 100
            else:
                games.append(False)
        else:
            if row['prediction_score'] > draw_prob:
                games.append(True)
                if row['Resultat'] == 'Draw':
                    balance1 += (100/draw_prob -100)
                else:
                    balance1 -= 100
            else:
                games.append(False)
        balances.append(balance1)
    return balances, games

# Läser in filerna

df_ADA = pd.read_csv('ADAPredictions.csv')
df_DT = pd.read_csv('DTPredictions.csv')
df_ET = pd.read_csv('ETPredictions.csv')
df_GBC = pd.read_csv('GBCPredictions.csv')
df_KNN = pd.read_csv('KNNPredictions.csv')
df_LDA = pd.read_csv('LDAPredictions.csv')
df_LGBM = pd.read_csv('LGBMPredictions.csv')
df_LR = pd.read_csv('LRPredictions.csv')
df_NB = pd.read_csv('NBPredictions.csv')
df_QDA = pd.read_csv('QDAPredictions.csv')
df_RF = pd.read_csv('RFPredictions.csv')

all_df = [df_ADA, df_DT, df_ET, df_GBC, df_KNN, df_LDA, df_LGBM, df_LR, df_NB, df_QDA, df_RF]

# Tar fram medelvärde och standardavvikelse för den teoretiska normalfördelningen, och skriver ut dessa

for df in all_df:
    balances, games = find_balance(df)
    values = 0
    variance = 0
    betted = 0
    for index, row in df.iterrows():
        if games[index]:
            betted += 1
            home_prob = (1/float(row['HomeOdds']))
            away_prob = (1/float(row['AwayOdds']))
            draw_prob = (1/float(row['DrawOdds']))
            mean = 1/(home_prob+away_prob+draw_prob)
            values += (mean - 1)*100
            home_prob /= mean
            draw_prob /= mean
            away_prob /= mean
            mean = (mean-1)*100
            if row['Resultat'] == 'Win':
                variance += home_prob*((row['HomeOdds']-1)*100-mean)*((row['HomeOdds']-1)*100-mean)
                variance += (away_prob+draw_prob)*mean*mean
            elif row['Resultat'] == 'Loss':
                variance += away_prob*((row['AwayOdds']-1)*100-mean)*((row['AwayOdds']-1)*100-mean)
                variance += (home_prob+draw_prob)*mean*mean
            else:
                variance += draw_prob*((row['DrawOdds']-1)*100-mean)*((row['DrawOdds']-1)*100-mean)
                variance += (home_prob+away_prob)*mean*mean
    print(f"Mean: {10000 + values}, Std Deviation: {(variance)**0.5}")

print("Program finished as expected.")
