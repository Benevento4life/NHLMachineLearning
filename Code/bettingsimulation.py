
'''
Programmet läser in en .csv-fil med förutsägningar, och simulerar betting på datan den inte är tränad på.
Resultatet skrivs ut och plottas även mot en benchmark-strategi samt ett väntevärde, vidare beskrivit i rapporten.
Även slutbalansen och antalet matcher för varje simulering skrivs ut.
I nuläget sker en ofullständig simulering. Programmet kan lätt modifieras för att utföra den fullständiga istället.
Programmet tar inte input. Istället bes användaren skriva in namnet på filerna som ska läsas in i raderna 13-23.
'''

import pandas as pd
from matplotlib import pyplot as plt

# Läser in modellens förutsägningar

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

# Testar modellen och sparar resultaten

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

# Plottar simuleringarna

plt.figure(figsize=(12, 7))

plt.plot(find_balance(df_ADA)[0], label="Ada Boost Classifier")
plt.plot(find_balance(df_DT)[0], label="Decision Tree Classifier")
plt.plot(find_balance(df_ET)[0], label="Extra Trees Classifier")
plt.plot(find_balance(df_GBC)[0], label="Gradient Boosting Classifier")
plt.plot(find_balance(df_KNN)[0], label="K Neighbors Classifier")
plt.plot(find_balance(df_LDA)[0], label="Linear Discriminant Analysis")
plt.plot(find_balance(df_LGBM)[0], label="Light Gradient Boosting Machine")
plt.plot(find_balance(df_LR)[0], label="Logistic Regression")
plt.plot(find_balance(df_NB)[0], label="Naive Bayes")
plt.plot(find_balance(df_QDA)[0], label="Quadratic Discriminant Analysis")
plt.plot(find_balance(df_RF)[0], label="Random Forest Classifier")

plt.title("Balans över tid, Fullständig")
plt.xlabel("Antalet Matcher")
plt.ylabel("Balans")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Skriver ut resultaten

print([find_balance(df)[0][-1] for df in all_df])
print([len([x for x in find_balance(df)[1] if x]) for df in all_df])

print('Program finished as expected.')
