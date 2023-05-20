from flask import Flask, render_template, request, flash, session
import joblib
import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import calculate_bmi
import psycopg2  
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

# Załaduj model SVM
# svm_model = joblib.load('svm_model.pkl')
app.secret_key = 'cairocoders-ednalan'
 
conn = psycopg2.connect(host='localhost', port=5433, database='Diabetes', user='postgres', password='postgres')




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

questions_BMI = [
    "Podaj swoją wagę (kg):",
    "Podaj swój wzrost (m2):",
]
answers_BMI = []
@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    
        _hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        # cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # account = cursor.fetchone()
        # print(account)
        # # If account exists show error and validation checks
        # if account:
        #     flash('Account already exists!')
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     flash('Invalid email address!')
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     flash('Username must contain only characters and numbers!')
        # elif not username or not password or not email:
        #     flash('Please fill out the form!')
        # else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
        cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username, _hashed_password, email))
        conn.commit()
        flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')



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
            train_data = pd.read_csv('train.csv')

            test_data = pd.read_csv('test.csv')

            X_train = train_data.drop('Diabetes_012', axis=1)
            y_train = train_data['Diabetes_012']


            X_test = test_data.drop('Diabetes_012', axis=1)
            y_test = test_data['Diabetes_012']

            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            data = pd.DataFrame(new_data, columns=X_train.columns)
            prediction = model.predict(data)
            # prediction = SVC.predict([answers])  
            if prediction == 2:
                result = "Istnieje ryzyko, że jesteś chory na cukrzycę typu 2."
            else:
                result = "Ryzyko cukrzycy typu 2 jest niskie."
        print(result)
            # return render_template('result.html', result=result)

    
    return render_template('index.html', question=questions[0])


@app.route('/', methods=['GET','POST'])
def gender():
    return render_template('main.html')

@app.route('/bmi', methods=['GET','POST'])
def calculate():
    if request.method == 'POST':
        user_answer_BMI = request.form['answer_BMI']
        answers_BMI.append(user_answer_BMI)
        
        if len(answers_BMI) < len(questions_BMI):
            return render_template('bmi.html', question_BMI=questions_BMI[len(answers_BMI)])
        else:  
            weight = answers_BMI[0]
            height = answers_BMI[1]
            bmi = calculate_bmi.calculate_bmi.calculate_bmi(weight, height)
        print(bmi)
        # return render_template('bmi_result.html',bmi=bmi)

    return render_template('bmi.html', question_BMI=questions_BMI[0])















if __name__ == '__main__':
    app.run()