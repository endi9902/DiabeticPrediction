from flask import Flask, render_template, request
import joblib
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
    # Dodaj kolejne pytania tutaj
]

# Inicjalizuj zmienną przechowującą odpowiedzi
answers = []

@app.route('/form', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Zapisz odpowiedź użytkownika
        user_answer = request.form['answer']
        answers.append(user_answer)
        
        # Przejdź do kolejnego pytania lub wykonaj analizę
        if len(answers) < len(questions):
            return render_template('index.html', question=questions[len(answers)])
        else:
            # Wykonaj analizę przy użyciu algorytmu SVM
            # prediction = svm_model.predict([answers])  # Przykład przekazania odpowiedzi jako wektora cech dla SVM
            # Zwróć odpowiedź na podstawie wyniku analizy
            # if prediction == 1:
            #     result = "Istnieje ryzyko, że jesteś chory na cukrzycę typu 2."
            # else:
            #     result = "Ryzyko cukrzycy typu 2 jest niskie."
            
            # Wyświetl wynik użytkownikowi
            return render_template('result.html', result=result)
    
    return render_template('index.html', question=questions[0])


@app.route('/', methods=['GET','POST'])
def gender():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()