
'''
Programmet läser in ett dataset i form av en .csv-fil och tränar sedan en ML-modell på att förutse resultaten av matcherna i datasetet.
Programmet skriver ut viktiga metrics och visar även modellens confusion matrix.
Slutligen testas modellen på de sista 20% av datan. Dessa förutsägningar, samt modellen, sparas.
Programmet tar inte input. Användaren tillbes därmed själv skriva in namn på filer i rad 15, 72 och 76.
Programmet bygger som nu skrivit en Logistic Regression-modell. Detta kan även ändras genom att modifiera rad 50 och 51.
'''

import pandas as pd
from pycaret.classification import *

# Laddar in datan

dataset = pd.read_csv('processedData.csv') # Byt ut filnamnet om du så önskar

# Delar in datan i två delar. 80% används för träning och 20% för simulering av betting

dataset.sort_values(['gameDate'])

split_point = int(len(dataset) * 0.8)

dataset_80 = dataset[:split_point]
dataset_20 = dataset[split_point:]  

dataset_80 = dataset_80.reset_index(drop=True)

# Delar upp datan

data = dataset_80.sample(frac=0.9, random_state=786).reset_index(drop=True)
data_unseen = dataset_80.drop(data.index).reset_index(drop=True)

# Skriver ut information om datan

print('Data for Modeling: ' + str(data.shape))
print('Unseen Data For Predictions: ' + str(data_unseen.shape))

# Utför setup med Resultat som target
exp_mclf101 = setup(data=data, target='Resultat', session_id=123, normalize=True, normalize_method='zscore', ignore_features=['gameId', 'index', 'HomeOdds', 'DrawOdds', 'AwayOdds'])

# Nedan kommenterat är koden för jämförning av modeller. Ta bort kommentering för jämförande av modeller

'''
compare_models()
exit()
'''

# Skapar och tunar modellen

model = create_model('lr') # Byt ut argumentet för annan modell
model = tune_model(model, n_iter = 10) # Ändra n_iter eller kommentera bort om det behövs

# Visar modellens confusion matrix

plot_model(model, plot = 'confusion_matrix') 

# Skriver ut modellens förutsägningar av den dolda datan

predict_model(model)

# Tränar modellen på den dolda datan

model = finalize_model(model)

# Testar modellen på de sista 20% av datan, och skriver ut resultat

unseen_predictions = predict_model(model, data=dataset_20)
unseen_predictions.head()

# Sparar förutsägningarna på de sista 20%

unseen_predictions.to_csv('LRPredictions.csv') # Byt filnamn om du så önskar

# Sparar modellen som en .pkl-fil

save_model(model, 'LRModel') # Byt ut filnamnet om du så önskar

print("Program finished as expected.")
