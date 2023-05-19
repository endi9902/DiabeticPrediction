import pandas as pd

# Wczytanie danych z pliku CSV do ramki danych
df = pd.read_csv('baza.csv')

# Lista nazw kolumn do usunięcia
kolumny_do_usuniecia = ['HighChol', 'CholCheck', 'Stroke', 'HeartDiseaseorAttack', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'DiffWalk', 'Education',  'Income' ]

# Usuwanie kolumn
df = df.drop(kolumny_do_usuniecia, axis=1)

# Nowa kolejność nazw kolumn
nowa_kolejnosc = ['Sex', 'Age', 'HighBP', 'BMI', 'Smoker', 'PhysActivity', 'Fruits', 'Veggies', 'GenHlth', 'MentHlth', 'PhysHlth', 'Diabetes_012']

# Zmiana kolejności kolumn
df = df[nowa_kolejnosc]

df.to_csv('baza-preprocessing.csv', index=False)

df_new = pd.read_csv('baza-preprocessing.csv')
czy_brakujace_wiersze = df_new.isnull().any(axis=1)
wiersze_brakujace = df[czy_brakujace_wiersze]
print(wiersze_brakujace)
# print(df)
