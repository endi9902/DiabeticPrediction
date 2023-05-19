import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


train_data = pd.read_csv('train.csv')

test_data = pd.read_csv('test.csv')

X_train = train_data.drop('Diabetes_012', axis=1)
y_train = train_data['Diabetes_012']


X_test = test_data.drop('Diabetes_012', axis=1)
y_test = test_data['Diabetes_012']

model = RandomForestClassifier()


model.fit(X_train, y_train)


y_pred = model.predict(X_test)

new_data = pd.DataFrame([[0, 40, 1, 25, 1, 1, 3, 2, 3, 2, 0]], columns=X_test.columns)
prediction = model.predict(new_data)
print("Przewidywany status cukrzycowy:", prediction)