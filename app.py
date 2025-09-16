from flask import Flask, render_template, request, url_for, redirect, session, flash
from werkzeug.security import check_password_hash as hash_check, generate_password_hash as hash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app=Flask(__name__)
app.secret_key='hello'
app.permanent_session_lifetime=timedelta(days=3)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/flaskDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

#__________________________________________________________________________________________

class student(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    stud_email=db.Column(db.String(100),unique=True,nullable=False)
    stud_pass=db.Column(db.String(100),nullable=False)

    def __init__(self,stud_email,stud_pass):
        self.stud_email=stud_email
        self.stud_pass=stud_pass


with app.app_context():
    db.create_all()
#__________________________________________________________________________________________

@app.route('/',methods=['POST','GET'])          
def index():
        return render_template('signup.html')

# The code block below is the watchdog for the code block above
# Basically checks all the actions of '/'

@app.route('/signup_check',methods=['POST','GET'])          
def signup_check():
        if request.method=='POST':
              email=request.form.get('email')
              password=request.form.get('password')
              hash_password=hash(password)
              session['email']=email
            #   if email and password in db:
            #     return 'You already have an account'
            #   elif  email and passord not in db:
            #        create a new row in db

              print(f'Email : {email}')
              print(f'Password : {password}')
              return redirect(url_for('dashboard'))
            #   if email in db: 
            #     db.session.add(student(email,password))
            #     db.session.commit()
            #     return redirect(url_for('dashboard'))
        else:
            return render_template('index.html')

#__________________________________________________________________________________________

@app.route('/signin',methods=['POST','GET'])          
def signin():
        return render_template('signin.html')

# The code block below is the watchdog for the code block above
# Basically checks all the actions of '/signin'


@app.route('/signin_check',methods=['POST','GET'])          
def signin_check():
    if request.method=='POST':
         if 'email' in session:
              return redirect(url_for('dashboard'))
         else:
            email=request.form.get('email')
            password=request.form.get('password')
            # if hash_check(db_password,password):
            session['email']=email
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index'))
#__________________________________________________________________________________________

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')
#__________________________________________________________________________________________






if __name__=='__main__':
    app.run(debug=True)
