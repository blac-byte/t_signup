from flask import Flask, render_template, request, url_for, redirect, session, flash
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
    id=db.Column(db.Integer,primary_key=True)
    stud_email=db.Column(db.String(100), primary_key=True)
    stud_pass=db.Column(db.String(100))

    def __init__(self,stud_email,stud_pass):
        self.stud_email=stud_email
        self.stud_pass=stud_pass


with app.app_context():
    db.create_all()
#__________________________________________________________________________________________

@app.route('/',methods=['POST','GET'])          
def index():
        return render_template('signup.html')

#__________________________________________________________________________________________


@app.route('/page',methods=['GET','POST'])
def page():
       if request.method=='POST':
            get_email=request.form.get('email')
            get_pass=request.form.get('password')
            db.session.add(student(get_email,get_pass))
            db.session.commit()
            return f'{get_email} {get_pass}'
       else:
            return render_template('page.html')
#__________________________________________________________________________________________






if __name__=='__main__':
    app.run(debug=True)
