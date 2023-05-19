import pandas as pd
from sklearn.model_selection import train_test_split

# Wczytanie danych z pliku CSV
df = pd.read_csv('baza-preprocessing.csv')

# Podział danych na zbiór treningowy i testowy
train_data, test_data = train_test_split(df, test_size=0.3, random_state=42)

# Zapis danych treningowych do pliku CSV
train_data.to_csv('train.csv', index=False)

# Zapis danych testowych do pliku CSV
test_data.to_csv('test.csv', index=False)
