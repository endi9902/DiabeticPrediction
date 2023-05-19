import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Wczytanie danych treningowych z pliku CSV
train_data = pd.read_csv('train.csv')

# Wczytanie danych testowych z pliku CSV
test_data = pd.read_csv('test.csv')

# Podział danych treningowych na cechy (X) i etykiety (y)
X_train = train_data.drop('Diabetes_012', axis=1)
y_train = train_data['Diabetes_012']

# Podział danych testowych na cechy (X) i etykiety (y)
X_test = test_data.drop('Diabetes_012', axis=1)
y_test = test_data['Diabetes_012']

# Inicjalizacja modelu lasu losowego
model = RandomForestClassifier()

# Trenowanie modelu na danych treningowych
model.fit(X_train, y_train)

# Przewidywanie na danych testowych
y_pred = model.predict(X_test)

# Obliczenie dokładności modelu
accuracy = accuracy_score(y_test, y_pred)
print("Dokładność modelu:", accuracy)
