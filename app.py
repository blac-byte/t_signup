from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash as hash_check, generate_password_hash as hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user



app=Flask(__name__)
app.secret_key='hello'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"   # Redirect here if not logged in

# Database connector
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/flaskdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


#__________________________________________________________________________________________

app.config['SESSION_COOKIE_HTTPONLY'] = True   # JS can't read cookies
app.config['SESSION_COOKIE_SECURE'] = True     # only send cookies over HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # protect against CSRF

#__________________________________________________________________________________________


# Database frame/ skeleton
class student_db(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.Text,nullable=True)

    def __init__(self,email,password):
        self.email=email
        self.password=password


with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin" #-------------------------------- redirects here if not logged in

@login_manager.user_loader
def load_user(user_id):
    return student_db.query.get(int(user_id))

#__________________________________________________________________________________________

@app.route('/',methods=['POST','GET'])          
def signup():
        return render_template('signup.html')

# The code block below is the watchdog for the code block above
# Basically checks all the actions of '/'

@app.route('/signup_check',methods=['POST','GET'])          
def signup_check():
        if request.method=='POST':
            email=request.form.get('email').strip().lower()
            password=request.form.get('password')
            hash_password=hash(password)
            user=student_db.query.filter_by(email=email).first()
            if user:  #----------------------------------- checks for existing email in db with no password
                if user.password is None: #--------------- checks if account has been initialized
                    user.password=hash_password
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('dashboard'))
                else:
                    return '<h1>Acc already exists<h1>'
            else:
              return '<h1>No acc<h1>'
        else:
              return redirect(url_for('index'))

#__________________________________________________________________________________________

@app.route('/signin',methods=['POST','GET'])          
def signin():
        return render_template('signin.html')

# The code block below is the watchdog for the code block above
# Basically checks all the actions of '/signin'


@app.route('/signin_check',methods=['POST'])          
def signin_check():
    if request.method=='POST':
        if current_user.is_authenticated:
             return redirect(url_for('dashboard'))
        email=request.form.get('email').strip().lower()
        password=request.form.get('password')
        user=student_db.query.filter_by(email=email).first()
        if user and hash_check(user.password,password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('signin'))
        
    else:
        return redirect(url_for('signin'))
#__________________________________________________________________________________________

@app.route('/dashboard', methods=['GET','POST'])

def dashboard():
    if request.method=='POST':
        theory={}
        lab={}
        theory_start, theory_end = None, None
        lab_start, lab_end = None, None
        day = None
        raw_text=request.form.get('table')
        rows=raw_text.splitlines()
        for row in rows:
            part=row.split('\t')
            if part[0]=='THEORY' and part[1]=='Start':
                 theory_start=part[2:]
                 print(theory_start)
            elif part[0]=='End':
                 theory_end=part[1:]
                 print(theory_end)
            elif part[0]=='LAB' and part[1]=='Start':
                 lab_start=part[2:]
                 print(lab_start)
            elif part[0]=='End' and not lab_end:
                 lab_end=part[1:]
                 print(lab_end)
            elif part[0] in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
                 day=part[0]
                 theory[day]=part[2:]
                 
            elif part[0]=='LAB' and day:
                 lab[day]=part[1:]
        print(f'day {theory}')
        print(f'lab {lab}')

        print('___________________________________________________')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html')
#__________________________________________________________________________________________

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
     if request.method=='POST':
          logout_user()
          flash("You have been logged out successfully!", "info")
          return redirect(url_for('signin'))





if __name__=='__main__':
    app.run(debug=True)
