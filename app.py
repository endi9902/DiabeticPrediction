from flask import Flask, render_template, request
import joblib
import pandas as pd
from sklearn.svm import SVC
app = Flask(__name__)

# Załaduj model SVM
# svm_model = joblib.load('svm_model.pkl')

# Lista pytań
questions = [
    "Wybierz płeć:",
    "Wpisz swój wiek:",
    "Czy masz wysokie ciśnienie krwi?",
    "Wpisz swoje BMI. Możesz je obliczyć w zakładce BMI.",
    "Czy palisz papierosy?",
    "Czy uprawiasz jakąś aktywność fizyczną?",
    "Czy uwzględniasz w swojej diecie świeże owoce?",
    "Czy uwzględniasz w swojej diecie świeże warzywa?",
    "Jakie jest twoje ogólne samopoczucie w skali od 0 do 5?",
    "Jakie jest twoje psychiczne samopoczucie w skali od 0 do 30?",
    "Jakie jest twoje samopoczucie fizyczne w skali od 0 do 30?",
]
answers = []

@app.route('/form', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_answer = request.form['answer']
        answers.append(user_answer)
        
        if len(answers) < len(questions):
            return render_template('index.html', question=questions[len(answers)])
        else:
            data = pd.DataFrame(columns=['Sex', 'Age', 'HighBP', 'BMI', 'Smoker', 'PhysActivity', 'Fruits', 'Veggies', 'GenHlth', 'MentHlth', 'PhysHlth'])
            sex = answers[0]
            age = answers[1]
            highBP = answers[2]
            bmi = answers[3]
            smoker = answers[4]
            physActivity = answers[5]
            fruits = answers[6]
            veggies = answers[7]
            genHlth = answers[8]
            mentHlth = answers[9]
            physHlth = answers[10]
            new_data = {'Sex': [sex], 'Age': [age], 'HighBP': [highBP], 'BMI':[bmi], 'Smoker': [smoker], 'PhysActivity':[physActivity], 'Fruits': [fruits], 'Veggies':[veggies], 'GenHlth':[genHlth], 'MentHlth':[mentHlth], 'PhysHlth':[physHlth] }
            data = pd.DataFrame(new_data)
            # prediction = SVC.predict([answers])  
            # if prediction == 1:
            #     result = "Istnieje ryzyko, że jesteś chory na cukrzycę typu 2."
            # else:
            #     result = "Ryzyko cukrzycy typu 2 jest niskie."
            
            # return render_template('result.html', result=result)
            print("Wprowadzone dane:")
            print(data)
    
    return render_template('index.html', question=questions[0])


@app.route('/', methods=['GET','POST'])
def gender():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()