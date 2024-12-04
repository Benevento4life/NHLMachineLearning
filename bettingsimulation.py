
'''
Programmet läser in en .csv-fil med förutsägningar, och simulerar betting på datan den inte är tränad på.
Resultatet skrivs ut och plottas även mot en benchmark-strategi samt ett väntevärde, vidare beskrivit i rapporten.
Programmet tar inte input. Istället bes användaren skriva in namnet på filen som ska läsas in i rad 17.
'''

import pandas as pd
from matplotlib import pyplot as plt

games = 0
bets = 0
wins = 0

# Läser in modellens förutsägningar

df = pd.read_csv('examplePredictions.csv') # Byt ut filnamnet om du så önskar

# Testar modellen och sparar resultaten

balance1 = 10000
balances = [10000]

for index, row in df.iterrows():
    home_prob = (1/float(row['HomeOdds']))
    away_prob = (1/float(row['AwayOdds']))
    draw_prob = (1/float(row['DrawOdds']))
    if row['prediction_label'] == 'Win':
        if row['prediction_score'] > home_prob:
            if row['Resultat'] == 'Win':
                balance1 += 100/home_prob -100
                wins += 1
            else:
                balance1 += -100
            bets += 1
    elif row['prediction_label'] == 'Loss':
        if row['prediction_score'] > away_prob:
            if row['Resultat'] == 'Loss':
                balance1 += 100/away_prob -100
                wins += 1
            else:
                balance1 += -100
            bets += 1
    else:
        if row['prediction_score'] > draw_prob:
            if row['Resultat'] == 'Draw':
                balance1 += 100/draw_prob -100
                wins += 1
            else:
                balance1 += -100
            bets += 1
    balances.append(balance1)

# Testar benchmark-strategin och sparar resultatet

balance2 = 10000
balances2 = [10000]

for index, row in df.iterrows():
    home_prob = (1/float(row['HomeOdds']))
    away_prob = (1/float(row['AwayOdds']))
    draw_prob = (1/float(row['DrawOdds']))
    if home_prob == min(home_prob,away_prob,draw_prob):
        if row['Resultat'] == 'Win':
            balance2 += 100/home_prob -100
        else:
            balance2 += -100
        bets += 1
    elif away_prob == min(home_prob,away_prob,draw_prob):
        if row['Resultat'] == 'Loss':
            balance2 += 100/away_prob -100
        else:
            balance2 += -100
        bets += 1
    else:
        if row['Resultat'] == 'Draw':
            balance2 += 100/draw_prob -100
        else:
            balance2 += -100
        bets += 1
    balances2.append(balance2)

# Simulerar väntevärdet av bettingen och sparar resultatet

balance3 = 10000
balances3 = [10000]

for index, row in df.iterrows():
    home_prob = (1/float(row['HomeOdds']))
    away_prob = (1/float(row['AwayOdds']))
    draw_prob = (1/float(row['DrawOdds']))
    implied_prob = home_prob+away_prob+draw_prob
    balance3 += 100/implied_prob-100
    balances3.append(balance3)
    games += 1

print(f"The model ended with {balance1} units after starting with 10000 units.")
print(f"It made {bets} bet out of {games} and won {wins} times.")
print(f"A benchmark model ended with {balance2} units, and the expected value after betting randomly is {balance3}.")

# Plottar simuleringarna

plt.figure(figsize=(10, 6))
plt.plot(balances, label="Model Strategy")
plt.plot(balances2, label="Benchmark Strategy")
plt.plot(balances3, label="Expected Value (Random)")
plt.title("Betting Balance Over Games")
plt.xlabel("Number of Games")
plt.ylabel("Balance")
plt.legend()
plt.grid(True)
plt.show()

print('Program finished as expected.')
